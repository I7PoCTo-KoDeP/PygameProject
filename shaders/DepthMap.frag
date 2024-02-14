#version 330 core

in vec2 uv;

uniform sampler2D tex;
uniform float angle = 90;
uniform float offset;

out vec4 color;

void main()
{//uv.x > sin(angle / 7) * uv.y + offset
        vec2 new_uv;
        vec3 COLOR;
        if(uv.x < sin(angle) * uv.y && uv.x > sin(angle) * uv.y - 0.2 && uv.x < sin(radians(45)) / uv.y)
        {
                COLOR = vec3(0.1, 0.1, 0.1);
        }
        else
        {
                COLOR = texture(tex, uv).rgb + offset * 0;
        }
        new_uv.x = uv.x + sin(angle) * uv.y;
        new_uv.y = uv.y + sin(angle) * uv.y;
        vec4 other_color = texture(tex, new_uv);
        color = vec4(COLOR, 1.0);
}