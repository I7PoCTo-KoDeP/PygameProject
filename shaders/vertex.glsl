#version 330 core

layout (location=0) in vec3 vertexPos;
layout (location=1) in vec2 vertexTexCoord;
uniform float in_angle;

out vec2 fragmentTexCoord;

void main()
{
    vec2 new_vertexPos;
    float angle;
    angle = sin(in_angle);
    new_vertexPos.x = vertexPos.x + angle * (1.0 - vertexTexCoord.y);
    new_vertexPos.y = vertexPos.y + angle * (1.0 - vertexTexCoord.y);
    fragmentTexCoord = vertexTexCoord;
    gl_Position = vec4(new_vertexPos, 0.0, 1.0);
}