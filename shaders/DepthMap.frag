#version 330 core

in vec2 uv;

uniform sampler2D tex;
uniform float angle = 75;
uniform vec2 topRight;
uniform vec2 bottomLeft;
uniform vec3 COLOR;
uniform float brightness;
uniform float cutoff = 0.4;

out vec4 color;

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
        vec2 ray1 = vec2(newUv.x * rotatedRay.y - newUv.y * rotatedRay.x - 0.1, newUv.x * rotatedRay.y - newUv.y * rotatedRay.x);
        vec2 ray2 = vec2(new_uv.x * firstRotatedRay.y - new_uv.y * firstRotatedRay.x + 0.1, new_uv.x * firstRotatedRay.y - new_uv.y * firstRotatedRay.x);

        if((ray1.y > 0 && ray1.x < 0) || (ray2.y < 0 && ray2.x > 0))
        {
                alpha = brightness + 2 * (ray1.y - ray1.x) + 2 * (ray2.x - ray2.y);
        }

        float cut = 1.0 - abs(uv.y - cutoff) + ray1.x - ray2.x + ray1.y - ray2.y;

        color = vec4(COLOR, alpha * cut * ray1.x);
}