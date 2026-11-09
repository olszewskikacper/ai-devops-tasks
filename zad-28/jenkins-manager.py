#!/usr/bin/env python3
"""Proste narzędzie CLI do zarządzania zadaniami Jenkins przez Jenkins REST API.

Funkcje:
  list              - lista wszystkich zadań (jobs)
  status [JOB]      - status ostatniego builda jednego lub wszystkich zadań
  build JOB         - uruchomienie zadania (opcjonalnie z parametrami)

Autoryzacja: nazwa użytkownika i token API ze zmiennych środowiskowych
JENKINS_URL, JENKINS_USER, JENKINS_API_TOKEN. Biblioteki: tylko standardowa.
"""

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

TIMEOUT = 15  # sekundy


class JenkinsError(Exception):
    """Błąd komunikacji z Jenkinsem lub nieprawidłowa odpowiedź."""


class JenkinsClient:
    def __init__(self, url, user, token):
        self.url = url.rstrip("/")
        credentials = base64.b64encode(f"{user}:{token}".encode()).decode()
        self.auth_header = f"Basic {credentials}"

    def _request(self, path, method="GET", headers=None, data=None):
        request = urllib.request.Request(
            f"{self.url}{path}", method=method, data=data
        )
        request.add_header("Authorization", self.auth_header)
        for key, value in (headers or {}).items():
            request.add_header(key, value)
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                return response.status, response.headers, response.read()
        except urllib.error.HTTPError as err:
            if err.code == 401:
                raise JenkinsError("401: nieprawidłowy login lub token API.") from err
            if err.code == 403:
                raise JenkinsError("403: brak uprawnień do tej operacji.") from err
            if err.code == 404:
                raise JenkinsError(f"404: nie znaleziono zasobu {path}.") from err
            raise JenkinsError(f"Błąd HTTP {err.code} dla {path}.") from err
        except urllib.error.URLError as err:
            raise JenkinsError(f"Brak połączenia z {self.url}: {err.reason}") from err
        except TimeoutError as err:
            raise JenkinsError(f"Przekroczono czas oczekiwania ({TIMEOUT}s).") from err

    def _get_json(self, path):
        _, _, body = self._request(path)
        try:
            return json.loads(body)
        except json.JSONDecodeError as err:
            raise JenkinsError("Jenkins zwrócił odpowiedź, która nie jest JSON-em.") from err

    @staticmethod
    def _job_path(name):
        """'folder/zadanie' -> '/job/folder/job/zadanie'."""
        parts = [urllib.parse.quote(p, safe="") for p in name.strip("/").split("/")]
        return "".join(f"/job/{p}" for p in parts)

    def list_jobs(self):
        data = self._get_json("/api/json?tree=jobs[name,color,url]")
        return data.get("jobs", [])

    def last_build(self, name):
        tree = "number,result,building,timestamp,duration,url"
        path = f"{self._job_path(name)}/lastBuild/api/json?tree={tree}"
        try:
            return self._get_json(path)
        except JenkinsError as err:
            if str(err).startswith("404"):
                return None  # zadanie nie ma jeszcze żadnego builda (lub nie istnieje)
            raise

    def _crumb_header(self):
        """Pobiera token CSRF (crumb). Jenkins bez CSRF zwraca 404, wtedy pomijamy."""
        try:
            data = self._get_json("/crumbIssuer/api/json")
        except JenkinsError as err:
            if str(err).startswith("404"):
                return {}
            raise
        return {data["crumbRequestField"]: data["crumb"]}

    def trigger_build(self, name, params=None):
        headers = self._crumb_header()
        if params:
            endpoint = "buildWithParameters"
            data = urllib.parse.urlencode(params).encode()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            endpoint = "build"
            data = b""
        status, response_headers, _ = self._request(
            f"{self._job_path(name)}/{endpoint}", method="POST", headers=headers, data=data
        )
        return status, response_headers.get("Location", "")


def describe_build(build):
    if build.get("building"):
        return "W TOKU"
    return build.get("result") or "BRAK WYNIKU"


def cmd_list(client, _args):
    jobs = client.list_jobs()
    if not jobs:
        print("Brak zadań.")
    for job in jobs:
        print(f"{job['name']}  [{job.get('color', '?')}]")


def cmd_status(client, args):
    names = [args.job] if args.job else [j["name"] for j in client.list_jobs()]
    for name in names:
        try:
            build = client.last_build(name)
            if build is None:
                print(f"{name}: brak buildów (lub zadanie nie istnieje)")
                continue
            print(f"{name}: #{build['number']} {describe_build(build)} ({build['duration']} ms)")
        except JenkinsError as err:
            print(f"{name}: {err}")


def cmd_build(client, args):
    params = {}
    for item in args.param or []:
        if "=" not in item:
            raise JenkinsError(f"Parametr '{item}' musi mieć postać KLUCZ=WARTOŚĆ.")
        key, value = item.split("=", 1)
        params[key] = value
    status, location = client.trigger_build(args.job, params or None)
    print(f"Uruchomiono '{args.job}' (HTTP {status}). Kolejka: {location or 'brak informacji'}")


def build_parser():
    parser = argparse.ArgumentParser(description="Zarządzanie zadaniami Jenkins.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="lista zadań").set_defaults(func=cmd_list)
    p_status = sub.add_parser("status", help="status ostatniego builda")
    p_status.add_argument("job", nargs="?", help="nazwa zadania (domyślnie wszystkie)")
    p_status.set_defaults(func=cmd_status)
    p_build = sub.add_parser("build", help="uruchom zadanie")
    p_build.add_argument("job", help="nazwa zadania, np. moj-projekt lub folder/zadanie")
    p_build.add_argument("-p", "--param", action="append", help="parametr KLUCZ=WARTOŚĆ (można powtarzać)")
    p_build.set_defaults(func=cmd_build)
    return parser


def main():
    args = build_parser().parse_args()
    url = os.environ.get("JENKINS_URL")
    user = os.environ.get("JENKINS_USER")
    token = os.environ.get("JENKINS_API_TOKEN")
    if not (url and user and token):
        sys.exit("Ustaw zmienne środowiskowe JENKINS_URL, JENKINS_USER i JENKINS_API_TOKEN.")
    try:
        args.func(JenkinsClient(url, user, token), args)
    except JenkinsError as err:
        sys.exit(f"Błąd: {err}")


if __name__ == "__main__":
    main()
