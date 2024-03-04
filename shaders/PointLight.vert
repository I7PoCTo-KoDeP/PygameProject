#version 330 core

layout (location=0) in vec2 vertexPos;
layout (location=1) in vec2 vertexTexCoord;

out vec2 uv;

mat2 rotate(float _angle)
{
    return mat2(vec2(cos(_angle), -sin(_angle)), vec2(sin(_angle), cos(_angle)));
}

void main()
{
    vec2 newPos = vec2(vertexPos.x + 4 * cos(radians(90)) * (1.0 - vertexTexCoord.y), vertexPos.y);
    gl_Position = vec4(newPos, 0.0, 1.0);
    uv = vertexTexCoord;
}