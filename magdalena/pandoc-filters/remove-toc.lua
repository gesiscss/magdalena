-- SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
-- SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
--
-- SPDX-License-Identifier: AGPL-3.0-or-later

function Div(element)
    if element.attr.attributes["custom-style"] == "toc 1" then
        return {}
    else
        return element
    end
end

function Header(element)
    if element.level == 1 then
        if element.attr.identifier == "contents" then
            return {}
        else
            return element
        end
    else
        return element
    end
end