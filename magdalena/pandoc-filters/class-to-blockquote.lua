-- SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
-- SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
--
-- SPDX-License-Identifier: AGPL-3.0-or-later

-- Lua filter to use HTML blockquote
function InsertBlockQuote(element)
    new_content = pandoc.BlockQuote(element.content)
    return pandoc.Div(new_content, element.attr)
end

function Div(element)
    for index, value in pairs(element.attr.classes) do
        if value == 'core-quote' then
            return InsertBlockQuote(element)
        end

        if value == 'core-quote-2' then
            return InsertBlockQuote(element)
        end

        if value == 'long-core-quote' then
            return InsertBlockQuote(element)
        end
    end

    return nil
end