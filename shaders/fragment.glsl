#version 330 core

in vec3 fragmentColor;
in vec2 fragmentTexCoord;

out vec4 color;

uniform sampler2D imageTexture;

void main()
{
        color = vec4(texture(imageTexture, fragmentTexCoord).rgb, 0.1);
}