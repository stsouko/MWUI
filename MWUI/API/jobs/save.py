# -*- coding: utf-8 -*-
#
#  Copyright 2016-2018 Ramil Nugmanov <stsouko@live.ru>
#  This file is part of MWUI.
#
#  MWUI is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
from flask_login import current_user
from flask_restful import marshal_with, marshal
from math import ceil
from .marshal import (TaskPostResponseFields, TaskGetResponseFields, TasksList, TaskDeleteResponseFields,
                      TaskStructureResponseFields, TaskStructureFields, SaveTaskFields, RecordsCountFields)
from .common import fetch_task, results_page, results_task
from ..common import DBAuthResource, swagger, request_arguments_parser, abort
from ...config import RESULTS_PER_PAGE
from ...constants import TaskType, TaskStatus
from ...models import Task


class SavedTask(DBAuthResource):
    @swagger.operation(
        nickname='saved',
        responseClass=TaskGetResponseFields.__name__,
        parameters=[dict(name='task', description='Task ID', required=True,
                         allowMultiple=False, dataType='str', paramType='path'),
                    dict(name='page', description='Results pagination', required=False,
                         allowMultiple=False, dataType='int', paramType='query')],
        responseMessages=[dict(code=200, message="modeled task"),
                          dict(code=401, message="user not authenticated"),
                          dict(code=403, message='user access deny. you do not have permission to this task'),
                          dict(code=404, message='invalid task id. perhaps this task has already been removed'),
                          dict(code=406, message='task status is invalid. only validation tasks acceptable')])
    @request_arguments_parser(results_page)
    def get(self, task, page=None):
        """
        Task with modeling results of structures with conditions

        all structures include only models with nonempty results lists.
        see /task/model get doc.
        """
        result = self.__get_task(task)
        structures = result.data
        if page:
            structures = structures[RESULTS_PER_PAGE * (page - 1): RESULTS_PER_PAGE * page]

        return dict(task=task, status=TaskStatus.PROCESSED.value, date=result.date.isoformat(), type=result.type.value,
                    user=current_user.id, structures=structures), 200

    @swagger.operation(
        nickname='delete',
        responseClass=TaskDeleteResponseFields.__name__,
        parameters=[dict(name='task', description='Task ID', required=True,
                         allowMultiple=False, dataType='str', paramType='path')],
        responseMessages=[dict(code=202, message="task deleted"),
                          dict(code=401, message="user not authenticated"),
                          dict(code=403, message='user access deny. you do not have permission to this task'),
                          dict(code=404, message='invalid task id. perhaps this task has already been removed')])
    @marshal_with(TaskDeleteResponseFields.resource_fields)
    def delete(self, task):
        """
        Delete task from db
        """
        result = self.__get_task(task)
        resp = dict(task=task, status=TaskStatus.PROCESSED, date=result.date, type=result.type, user=current_user)
        result.delete()
        return resp, 202

    @staticmethod
    def __get_task(task):
        result = Task.get(task=task)
        if not result:
            abort(404, message='Invalid task id. Perhaps this task has already been removed')

        if result.user.id != current_user.id:
            abort(403, message='User access deny. You do not have permission to this task')
        return result


class SavedTasksList(DBAuthResource):
    @swagger.operation(
        nickname='saved_list',
        parameters=[dict(name='page', description='Results pagination', required=False,
                         allowMultiple=False, dataType='int', paramType='query')],
        responseClass=TasksList.__name__,
        responseMessages=[dict(code=200, message="saved tasks"),
                          dict(code=400, message="page must be a positive integer or None"),
                          dict(code=401, message="user not authenticated")])
    @marshal_with(TasksList.resource_fields)
    @request_arguments_parser(results_page)
    def get(self, page=1):
        """
        Get current user's saved tasks
        """
        return list(Task.select(lambda x: x.user == current_user.get_user()).page(page, pagesize=RESULTS_PER_PAGE))

    @swagger.operation(
        nickname='save',
        responseClass=TaskPostResponseFields.__name__,
        parameters=[dict(name='task', description='Validated structure task id', required=True,
                         allowMultiple=False, dataType=SaveTaskFields.__name__, paramType='body')],
        responseMessages=[dict(code=201, message="modeled task saved"),
                          dict(code=401, message="user not authenticated"),
                          dict(code=403, message='user access deny. you do not have permission to this task'),
                          dict(code=404, message='invalid task id. perhaps this task has already been removed'),
                          dict(code=406, message='task status is invalid. only modeled tasks acceptable'),
                          dict(code=406, message='task type is invalid. only modeling tasks acceptable'),
                          dict(code=409, message='task already exists in db'),
                          dict(code=500, message="modeling server error"),
                          dict(code=512, message='task not ready')])
    @marshal_with(TaskPostResponseFields.resource_fields)
    @request_arguments_parser(results_task)
    @fetch_task(TaskStatus.PROCESSED)
    def post(self, task, job, ended_at):
        """
        Store in database modeled task

        only modeled tasks can be saved.
        failed models in structures skipped.
        """
        if job['type'] != TaskType.MODELING:
            abort(406, message='task type is invalid. only modeling tasks acceptable')

        if Task.exists(task=task):
            abort(409, message='task already exists in db')
        data = marshal(job['structures'], TaskStructureResponseFields.resource_fields)
        Task(data, type=job['type'], date=ended_at, user=current_user.get_user(), task=task)

        return dict(task=task, status=TaskStatus.PROCESSED, date=ended_at, type=job['type'], user=current_user), 201


class SavedTasksCount(DBAuthResource):
    @swagger.operation(
        nickname='tasks_count',
        responseClass=RecordsCountFields.__name__,
        responseMessages=[dict(code=200, message="saved data"),
                          dict(code=401, message="user not authenticated"),
                          dict(code=403, message="user access deny")])
    def get(self):
        """
        Get user's saves count
        """
        q = Task.select(lambda x: x.user == current_user.get_user()).count()
        return dict(data=q, pages=ceil(q / RESULTS_PER_PAGE))
