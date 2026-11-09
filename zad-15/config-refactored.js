const CONFIGS = {
  development: {
    apiUrl: 'http://localhost:3000/api',
    debug: true,
    timeout: 5000
  },
  testing: {
    apiUrl: 'http://test-server:3000/api',
    debug: true,
    timeout: 5000
  },
  staging: {
    apiUrl: 'https://staging.example.com/api',
    debug: false,
    timeout: 10000
  },
  production: {
    apiUrl: 'https://api.example.com',
    debug: false,
    timeout: 15000
  }
};

const DEFAULT_ENV = 'development';

function getEnvironmentConfig(env) {
  const config = Object.hasOwn(CONFIGS, env) ? CONFIGS[env] : CONFIGS[DEFAULT_ENV];
  return { ...config };
}

module.exports = getEnvironmentConfig;
