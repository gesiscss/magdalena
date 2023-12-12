function Div(element)
    new_attributes = {}
    new_class = {}
    for key, value in pairs(element.attr.attributes) do
        if key == 'custom-style' then
            new_class[1] = string.gsub(
                string.lower(value),
                ' ',
                '-'
            )
        else
            new_attributes[key] = value
        end
    end

    return pandoc.Div(
        element.content,
        pandoc.Attr(element.attr.identifier, new_class, new_attributes)
    )
end

function Span(element)
    new_attributes = {}
    new_class = {}
    for key, value in pairs(element.attr.attributes) do
        if key == 'custom-style' then
            new_class[1] = string.gsub(
                string.lower(value),
                ' ',
                '-'
            )
        else
            new_attributes[key] = value
        end
    end

    return pandoc.Span(
        element.content,
        pandoc.Attr(element.attr.identifier, new_class, new_attributes)
    )
end
