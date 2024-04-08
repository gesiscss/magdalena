-- SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
-- SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
--
-- SPDX-License-Identifier: AGPL-3.0-or-later

function Span(element)
    for key, value in pairs(element.attributes) do
        if key == "custom-style" and value == "Hyperlink" then
            return element.content
        end
    end

    return element
end
