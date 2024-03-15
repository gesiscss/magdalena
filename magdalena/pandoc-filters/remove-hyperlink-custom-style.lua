function Span(element)
    for key, value in pairs(element.attributes) do
        if key == "custom-style" and value == "Hyperlink" then
            return element.content
        end
    end

    return element
end
