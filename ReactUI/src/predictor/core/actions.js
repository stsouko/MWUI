import * as CONST from './constants';

// Index page actions
export const addStructureIndex = obj => ({
  type: CONST.ADD_STRUCTURE_INDEX, obj,
});

export const deleteStructureIndex = structure => ({
  type: CONST.DELETE_STRUCTURE_INDEX, structure,
});

export const editStructureIndex = (structure, obj) => ({
  type: CONST.EDIT_STRUCTURE_INDEX, structure, obj,
});


// Validate page actions
export const addStructuresValidate = arr => ({
  type: CONST.ADD_STRUCTURES_VALIDATE, arr,
});

export const addStructuresResult = arr => ({
  type: CONST.ADD_STRUCTURE_RESULT, arr,
});

export const editStructureValidate = obj => ({
  type: CONST.EDIT_STRUCTURE_VALIDATE, obj,
});

export const addTasksSavePage = tasks => ({
  type: CONST.ADD_TASKS, tasks,
});

export const addOneTaskSavePage = task => ({
  type: CONST.ADD_TASK, task,
});

export const addSavedTaskContent = (task, content) => ({
  type: CONST.ADD_TASK_CONTENT, task, content,
});

export const addSavedTaskPages = pages => ({
  type: CONST.ADD_SAVED_TASK_PAGES, pages,
});

export const deleteSavedTaskPages = task => ({
  type: CONST.DELETE_SAVED_TASK_PAGES, task,
});

// Process page

export const addProcess = task => ({
  type: CONST.ADD_PROCESS, task,
});

export const finishProcess = task => ({
  type: CONST.FINISH_PROCESS, task,
});

