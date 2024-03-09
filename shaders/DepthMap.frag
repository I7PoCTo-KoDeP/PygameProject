#version 330 core

in vec2 uv;

uniform sampler2D tex;
uniform float angle = 75;
uniform vec2 topRight;
uniform vec2 bottomLeft;
uniform vec3 COLOR;
uniform float brightness;
uniform float cutoff = 0.4;
uniform float dist;
uniform float time;

out vec4 color;

float random(vec2 _uv) {
        return fract(sin(dot(_uv.xy, vec2(12.9898, 78.233))) * 43758.5453123);
}

float noise (in vec2 uv) {
        vec2 i = floor(uv);
        vec2 f = fract(uv);

        float a = random(i);
        float b = random(i + vec2(1.0, 0.0));
        float c = random(i + vec2(0.0, 1.0));
        float d = random(i + vec2(1.0, 1.0));

        vec2 u = f * f * (3.0 - 2.0 * f);

        return mix(a, b, u.x) + (c - a)* u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
}

vec2 rotate(vec2 ray, float angle)
{
        float b = ray.x - ray.y / tan(angle);
        return vec2(b, 0);
}

void main()
{
        float alpha = 0.0;
        vec2 firstRay = bottomLeft;
        vec2 secondRay = topRight;
        vec2 firstPoint = rotate(firstRay, radians(angle));
        vec2 secondPoint = rotate(secondRay, radians(angle));
        vec2 firstRotatedRay = firstRay - firstPoint;
        vec2 rotatedRay = secondRay - secondPoint;
        vec2 newUv = uv - secondPoint;
        vec2 new_uv = uv - firstPoint;
        float rand = noise(vec2(dist * time, 0.0));
        vec2 ray1 = vec2(newUv.x * rotatedRay.y - newUv.y * rotatedRay.x - 0.1 * rand, newUv.x * rotatedRay.y - newUv.y * rotatedRay.x);
        vec2 ray2 = vec2(new_uv.x * firstRotatedRay.y - new_uv.y * firstRotatedRay.x + 0.1 * rand, new_uv.x * firstRotatedRay.y - new_uv.y * firstRotatedRay.x);

        if((ray1.y > 0 && ray1.x < 0) || (ray2.y < 0 && ray2.x > 0))
        {
                alpha = brightness + 2 * (ray1.y - ray1.x) + 2 * (ray2.x - ray2.y);
        }

        float cut = 1.0 - abs(uv.y - cutoff) + ray1.x - ray2.x + ray1.y - ray2.y;

        color = vec4(COLOR, alpha * cut );
}