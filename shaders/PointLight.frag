#version 330 core

in vec2 uv;

out vec4 color;

uniform sampler2D tex;

void main()
{
        float alpha = (1.0 - abs(uv.y - 0.5)) * (1.0 - abs(uv.x - 0.5));
        float edge = pow(0.4, 2) - pow((0.5 - abs(0.5 - uv.y)), 2);
        if(uv.x > 0.5 - edge && uv.x < edge + 0.5)
        {
                alpha = 0.5;
        }

        color = vec4(texture(tex, uv).rgb, alpha);
}