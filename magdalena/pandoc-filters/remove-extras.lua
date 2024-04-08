-- SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
-- SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
--
-- SPDX-License-Identifier: AGPL-3.0-or-later

-- Lua filter to remove extra div elements from the AST
function Div(element)
    for index, value in pairs(element.attr.classes) do
        if value == 'cite-as-heading' then
            return {}
        end

        if value == 'license-heading' then
            return {}
        end
    end

    return nil
end