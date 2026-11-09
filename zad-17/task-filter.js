/**
 * Zwraca tytuły zakończonych zadań posortowane rosnąco według id.
 *
 * @param {Array<{id: number, title: string, status: string}>} tasks - Lista zadań.
 * @returns {string[]} Tytuły zadań o statusie "completed", w kolejności rosnącego id.
 */
function getCompletedTaskTitles(tasks) {
  return tasks
    .filter(task => task.status === 'completed')
    .sort((a, b) => a.id - b.id)
    .map(task => task.title);
}

module.exports = getCompletedTaskTitles;
