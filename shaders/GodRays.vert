#version 330 core

layout (location=0) in vec2 vertexPos;
layout (location=1) in vec2 vertexTexCoord;

//uniform float angle = radians(45);

out vec2 UV;
/*
mat2 rotate(float _angle){
    return mat2(vec2(cos(_angle), -sin(_angle)), vec2(sin(_angle), cos(_angle)));
}*/

void main()
{
    //vec2 new_vertexPos = vertexPos.xy;
    //vec2 new_vertexTexCoord;
    //new_vertexPos.x = vertexPos.x + 0 * (1.0 - vertexTexCoord.y);
    //new_vertexPos.y = vertexPos.y;
    //new_vertexTexCoord.x = vertexTexCoord.x;
    //new_vertexTexCoord.y = vertexTexCoord.y;

    gl_Position = vec4(vertexPos, 0.0, 1.0);
    UV = vertexTexCoord;
}