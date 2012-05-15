#ifndef HFPS_LEVEL_FORMAT_HPP
#define HFPS_LEVEL_FORMAT_HPP

#include <string>
#include <map>
#include <list>

struct LevelFile
{
    static const unsigned int VERSION = 0;
    static const unsigned int MAX_PATH_LENGTH = 64;
    static const char IDENT[8];

    struct Header
    {
        char ident[8]; //"HFPSLVL\0" - Hydra FPS Level
        unsigned int version;
        unsigned int numSurfaces;
    };

    struct Vertex
    {
        float coordinates[3];
        float uv[2];
    };

    struct Triangle
    {
        unsigned short indices[3];
    };

    struct Surface
    {
        Surface() :
            vertices(NULL),
            triangles(NULL)
        {}

        ~Surface()
        {
            delete[] vertices;
            delete[] triangles;
        }

        enum SurfaceFlags
        {
            sfSolid = 1 << 0, // Whether this surface is solid, as far as the Physics Engine is concerned
        };

        char texture[MAX_PATH_LENGTH]; // NULL-Terminated string containing texture name
        int flags; // Combination of Surface Flags
        unsigned short numVertices;
        unsigned short numTriangles;
        Vertex* vertices; // array with numVertices elements
        Triangle* triangles; // array with numTriangles elements
    };

    struct Entity
    {
        std::string classname;
        std::map<std::string, std::string> properties;
    };

    Header header;
    Surface* surfaces; //array with header.numSurfaces elements
    std::list<Entity> entities; //the rest of the file are entities in plain text - { "key" "value" "key" "value" ... } { "key" "value" ... } ...

    const bool loadFromFile(const std::string& filename);

    LevelFile();
    ~LevelFile();
};

#endif
