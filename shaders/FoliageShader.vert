#version 330 core

layout (location=0) in vec2 vertexPos;
layout (location=1) in vec2 vertexTexCoord;

uniform float wind_strengt = 0.3;
uniform float time;
uniform float speed = 1.0;

out vec2 uv;

float random(vec2 _uv) {
    return fract(sin(dot(_uv.xy, vec2(12.9898, 78.233))) * 43758.5453123);
}

float noise (in vec2 UV) {
    vec2 i = floor(UV);
    vec2 f = fract(UV);

    float a = random(i);
    float b = random(i + vec2(1.0, 0.0));
    float c = random(i + vec2(0.0, 1.0));
    float d = random(i + vec2(1.0, 1.0));

    vec2 u = f * f * (3.0 - 2.0 * f);

    return mix(a, b, u.x) + (c - a)* u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
}

void main()
{
    float wind = (noise(vec2(vertexTexCoord.x * time * speed)) - 0.5) * wind_strengt;
    vec2 newPos = vec2(vertexPos.x + wind * (1.0 - vertexTexCoord.y), vertexPos.y);
    uv = vertexTexCoord;
    gl_Position = vec4(newPos, 0.0, 1.0);
}