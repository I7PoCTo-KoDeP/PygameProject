#version 330 core
out vec4 FragColor;

struct Light
{
    vec3 direction;
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

in vec2 TexCoords;
in vec3 Normal;

uniform Light light;

void main()
{
    vec3 ambient = light.ambient;
    vec3 norm = normalize(Normal);
    vec3 lightDirection = normalize(-light.direction);
    float diff = max(dot(norm, lightDirection), 0.0);
    vec3 specular = light.specular;
    vec3 diffuse = light.diffuse * diff;

    vec3 res = ambient + diffuse + specular;
    FragColor = vec4(res, 1.0);
}