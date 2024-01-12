#version 330 core

layout (location=0) in vec3 vertexPos;
layout (location=1) in vec2 vertexTexCoord;

out vec2 fragmentTexCoord;

void main()
{
    vec2 new_vertexPos;
    float angle;
    fragmentTexCoord = vertexTexCoord;
    angle = cos(90);
    new_vertexPos.x = vertexPos.x + (1.0 - vertexTexCoord.y) * angle;
    new_vertexPos.y = vertexPos.y + angle * (1.0 - vertexTexCoord.y);
    gl_Position = vec4(new_vertexPos, 0.0, 1.0);
}