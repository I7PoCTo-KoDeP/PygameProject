#version 330 core

//in vec3 fragmentColor;
in vec2 UV;

uniform vec2 SCREEN_UV;
uniform sampler2D SCREEN_TEXTURE;

uniform float TIME;
uniform float angle = radians(0);
uniform float position = 0;
uniform float spread = 0.5;
uniform float cutoff = 0.3;
uniform float falloff = 0.6;
uniform float edge_fade = 0.15;

uniform float speed = 10.0;
uniform float ray1_density = 8.0;
uniform float ray2_density = 30.0;
uniform float ray2_intensity = 0.3;

uniform vec4 color = vec4(1.0, 0.9, 0.65, 0.2);

//uniform bool hdr = false;
uniform float seed = 5.0;

out vec4 COLOR;

/*struct Ray
{
    vec3 rayDirection;
    vec3 rayOrigin;
};*/

mat2 rotate(float _angle){
    return mat2(vec2(cos(_angle), -sin(_angle)), vec2(sin(_angle), cos(_angle)));
}

vec4 screen(vec4 base, vec4 blend){
	return 1.0 - (1.0 - base) * (1.0 - blend);
}

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

/*float intersection(Ray ray, vec4 p0)
{
    return -(dot(ray.rayOrigin, p0.xyz)) / dot(ray.rayDirection, p0.xyz);
}*/

void main()
{
	vec4 object = texture(SCREEN_TEXTURE, UV);
	//vec2 new_UV;
    //new_UV.x = UV.x + sin(angle) * UV.y;
    //new_UV.y = UV.y + sin(angle) * UV.y;
    //vec4 shadow = texture(SCREEN_TEXTURE, UV);

	vec2 transformed_uv = (rotate(angle) * (UV - position))  / ((UV.y + spread) - (UV.y * spread));

	vec2 ray1 = vec2(transformed_uv.x * ray1_density + sin(TIME * 0.1 * speed) * (ray1_density * 0.2) + seed, 1.0);
	vec2 ray2 = vec2(transformed_uv.x * ray2_density + sin(TIME * 0.2 * speed) * (ray1_density * 0.2) + seed, 1.0);

    float cut;
    cut = step(cutoff, 1.0 - object.a);

/*    if(object.a > 0)
    {
            cut = step(cutoff, 1.0 - object.a) * step(cutoff, 1.0 - shadow.a);
    }
    else
    {
        cut = 1.0;
    }*/

	ray1 *= cut;
	ray2 *= cut;

	float rays;

	rays = noise(ray1) + (noise(ray2) * ray2_intensity);

	rays *= smoothstep(0.0, falloff, (1.0 - UV.y)); // Bottom
	//rays *= smoothstep(0.0 + cutoff, edge_fade + cutoff, transformed_uv.x); // Left
	//rays *= smoothstep(0.0 + cutoff, edge_fade + cutoff, 1.0 - transformed_uv.x); // Right

	vec3 shine = vec3(rays) * color.rgb;

	shine = screen(texture(SCREEN_TEXTURE, UV), vec4(color)).rgb;

	COLOR = vec4(shine, rays * color.a);
}
