-- SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
-- SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
--
-- SPDX-License-Identifier: AGPL-3.0-or-later

-- Lua filter to convert Keyword paragraph into metadata
keywords = {}

-- Function to parse keyword Div
function parse_keywords(element)
    local new_keyword = nil

    -- We assume that the Div has a single paragraph
    for _, token in pairs(element.content[1].content) do
        if token.tag == "Str" then
            if token.text ~= "Keywords:" then
                if new_keyword == nil then
                    new_keyword = ""
                end
                
                new_keyword = new_keyword .. token.text
                
                if string.find(token.text, ",$") then
                    new_keyword = string.gsub(new_keyword, ",", "")
                    table.insert(keywords, new_keyword)
                    new_keyword = nil
                end
            end
        elseif token.tag == "Space" then
            if new_keyword ~= nil then
                new_keyword = new_keyword .. " "
            end
        end
    end

    if new_keyword ~= nil then
        table.insert(keywords, new_keyword)
    end
end

-- Filter to find keyword Div
function Div(element)
    for index, value in pairs(element.attr.classes) do
        if value == 'keywords' then
            parse_keywords(element)

            return {}
        end
    end

    return nil
end

-- Filter to add keywords to YAML header
function Meta(element)
    element.keywords = keywords

    return element
end