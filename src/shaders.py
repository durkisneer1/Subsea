vert_shader = '''
#version 330 core

in vec2 vert;
in vec2 texcoord;
out vec2 uvs;

void main() {
    uvs = texcoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}
'''

frag_shader = '''
#version 330 core

uniform sampler2D tex;
in vec2 uvs;

uniform float time = 0;
uniform vec2 offset = vec2(0, 0);
uniform vec2 speeds = vec2(256, 144);
uniform float causticStrength = 0.0;

const float distortionStrength = 0.0008;

void main() {
    // Caustics
    vec2 uv = uvs.xy + offset.xy / speeds.xy;
    vec4 k = vec4(time) * 0.8;
    k.xy = uv * 7.0;
    float val1 = length(
        0.5 - fract(k.xyw *= mat3(vec3(-2.0, -1.0, 0.0), vec3(3.0, -1.0, 1.0), vec3(1.0, -1.0, -1.0)) * 0.5)
    );
    float val2 = length(
        0.5 - fract(k.xyw *= mat3(vec3(-2.0, -1.0, 0.0), vec3(3.0, -1.0, 1.0), vec3(1.0, -1.0, -1.0)) * 0.2)
    );
    float val3 = length(
        0.5 - fract(k.xyw *= mat3(vec3(-2.0, -1.0, 0.0), vec3(3.0, -1.0, 1.0), vec3(1.0, -1.0, -1.0)) * 0.5)
    );
    vec4 color = vec4(pow(min(min(val1, val2), val3), 7.0) * causticStrength);

    // Distortion
    vec2 distortion = distortionStrength * vec2(
        cos((uvs.y + time / 60) * 20.0 + (uvs.x + time / 60) * 30.0),
        sin((uvs.x + time / 60) * 20.0 + (uvs.y + time / 60) * 30.0)
    );
    vec2 distortedCoords = uvs + distortion;
    vec4 distortedTexture = mix(texture(tex, distortedCoords), color, 0.3);

    // Output
    gl_FragColor = distortedTexture;
}
'''