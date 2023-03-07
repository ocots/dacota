using JSON


function calculateDiagram(c1, c2, c3, a, alpha)
  result = Dict("c1" => c1, "c2" => c2, "c3" => c3, "a" => a, "alpha" => alpha)
  json_result = JSON.json(result)
  return json_result
end



function read_json_file(filepath::AbstractString)
    # Open the file
    file = open(filepath, "r")

    # Read the contents of the file as a string
    contents = read(file, String)

    # Parse the JSON string
    json_content = JSON.parse(contents)

    # Close the file
    close(file)

    # Return the JSON dictionary
    return json_content
end
