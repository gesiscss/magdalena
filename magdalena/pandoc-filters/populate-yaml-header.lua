-- SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
-- SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
--
-- SPDX-License-Identifier: AGPL-3.0-or-later

-- Transfer some textual information to YAML metadata
issue_number = nil
title = nil
subtitle = nil
date = nil
cite_as = nil
license = nil
doi = nil

function Div(element)
    for index, value in pairs(element.attr.classes) do
        if value == 'reihentitel-guide' then
            for int_number in string.gmatch(pandoc.utils.stringify(element.content), "#%d+") do
                issue_number = string.gsub(int_number, '#', '')
            end
            return {}
        end

        if value == 'title' then
            title = pandoc.utils.stringify(element.content)
            return {}
        end

        if value == 'subtitle' then
            subtitle = pandoc.utils.stringify(element.content)
            return {}
        end

        if value == 'date' then
            date = pandoc.utils.stringify(element.content)
            return {}
        end

        if value == 'cite-as' then
            cite_as = pandoc.utils.stringify(element.content)
            return {}
        end

        if value == 'license' then
            license = pandoc.utils.stringify(element.content)
            return {}
        end

        if value == 'doi' then
            doi = pandoc.utils.stringify(element.content)
            return {}
        end
    end

    return nil
end

function Meta(element)
    if issue_number ~= nil then
        element.issue_number = issue_number
    end
    
    if title ~= nil then
        element.title = title
    end

    if subtitle ~= nil then
        element.subtitle = subtitle
    end

    if date ~= nil then
        element.date = date
    end

    if cite_as ~= nil then
        element.cite_as = cite_as
    end

    if license ~= nil then
        element.license = license
    end

    if doi ~= nil then
        element.doi = doi
    end

    return element
end