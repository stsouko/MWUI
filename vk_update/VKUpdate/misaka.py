# -*- coding: utf-8 -*-
#
#  Copyright 2019 Ramil Nugmanov <stsouko@live.ru>
#  This file is part of CIpress.
#
#  CIpress is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program; if not, see <https://www.gnu.org/licenses/>.
#
from misaka import HtmlRenderer


class MisakaRenderer(HtmlRenderer):
    def table(self, content):
        return f'<table class="table">{content}</table>'

    def paragraph(self, content):
        return f'<p class="para">{content}</p>'


__all__ = ['MisakaRenderer']
