# https://github.com/ndortega/Oxygen.jl
using Oxygen
using HTTP

include("calculateDiagram.jl")

struct ternaryMixture
    c1::Vector{Float64}
    c2::Vector{Float64}
    c3::Vector{Float64}
    a::Vector{Vector{Float64}}
    alpha::Vector{Vector{Float64}}
end


@get "/" function(request::HTTP.Request)
    return "Smith microservice in julia"
end

@post "/ternary-diagram" function(req::HTTP.Request)
    # https://ndortega.github.io/Oxygen.jl/stable/tutorial/request_body/
    mix = Oxygen.json(req, ternaryMixture)

    # diagram = calculateDiagram(mix.c1, mix.c2, mix.c3, mix.a, mix.alpha)

    diagram = read_json_file("graph.json")

    return diagram
end


serve(host="0.0.0.0", port=5000)
