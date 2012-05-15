#include <LevelFormat.hpp>
#include <fstream>
#include <iostream>
#include <algorithm>

// "HFPSLVL\0"
const char LevelFile::IDENT[8] = { 'H', 'F', 'P', 'S', 'L', 'V', 'L', '\0' };

namespace
{
    template<typename T, std::size_t len> const std::size_t getArrayLength(const T(&)[len])
    {
        return len;
    }
}

LevelFile::LevelFile():
    surfaces(NULL)
{
}

LevelFile::~LevelFile()
{
    delete[] surfaces;
}

const bool LevelFile::loadFromFile(const std::string& filename)
{
    //  Open for binary reading
    std::ifstream file(filename.c_str(), std::ios::binary|std::ios::in);
    if(file.fail())
    {
        std::cerr << "Could not open " << filename << "!" << std::endl;
        return false;
    }

    //  Read header
    file.read(reinterpret_cast<char*>(&header), sizeof(Header));
    if(file.fail())
    {
        std::cerr << filename << " is no valid level file, contains no header!" << std::endl;
        return false;
    }
    for(std::size_t i = 0; i < getArrayLength(header.ident); ++i)
    {
        if(header.ident[i] != IDENT[i])
        {
            std::cerr << filename << " is no valid level file, ident does not match!" << std::endl;
            return false;
        }
    }
    if(header.version != VERSION)
    {
        std::cerr << "level file " << filename << " has the wrong version (" << header.version << " should be " << VERSION << ")" << std::endl;
        return false;
    }

    //  Read surfaces
    surfaces = new Surface[header.numSurfaces];
    for(Surface* curSurf = surfaces; curSurf < surfaces + header.numSurfaces; ++curSurf)
    {
        file.read(reinterpret_cast<char*>(curSurf), sizeof(Surface) - sizeof(curSurf->vertices) - sizeof(curSurf->triangles));
        if(file.fail())
        {
            delete[] surfaces;
            std::cerr << "Error reading from level file " << filename << "!" << std::endl;
            return false;
        }
        curSurf->vertices = new Vertex[curSurf->numVertices];
        curSurf->triangles = new Triangle[curSurf->numTriangles];
        file.read(reinterpret_cast<char*>(&curSurf->vertices), curSurf->numVertices * sizeof(Vertex));
        file.read(reinterpret_cast<char*>(&curSurf->triangles), curSurf->numTriangles * sizeof(Triangle));
        if(file.fail())
        {
            delete[] surfaces;
            std::cerr << "Error reading from level file " << filename << "!" << std::endl;
            return false;
        }
    }

    //  Read entities (unknown number)
    enum State
    {
        sStart,
        sInEntity,
        sInKey,
        sPastKey,
        sInValue
    };
    State curState = sStart;
    Entity curEntity;
    std::string curKey;
    std::string curValue;
    while(true)
    {
        char c;
        file.get(c);
        // could not read?
        if(file.fail())
        {
            if(file.eof() && curState == sStart)
            {
                return true;
            }
            else
            {
                std::cerr << "Error reading entities from level file " << filename << "!" << std::endl;
                return false;
            }
        }
        switch(curState)
        {
        case sStart:
            switch(c)
            {
            case ' ':
            case '\t':
            case '\n':
                // ignore whitespaces
                break;
            case '{':
                curState = sInEntity;
                break;
            default:
                std::cerr << "Invalid Syntax in Entity part of level file " << filename << "!" << std::endl;
                return false;
            }
            break;

        case sInEntity:
            switch(c)
            {
            case ' ':
            case '\t':
            case '\n':
                //ignore whitespaces
                break;
            case '"':
                curState = sInKey;
                curKey.clear();
                break;
            case '}':
                if(curEntity.classname.empty())
                {
                    std::cout << "Warning: Entity without classname in level file " << filename << "!" << std::endl;
                }
                else
                {
                    entities.push_back(curEntity);
                }
                curState = sStart;
                break;
            default:
                std::cerr << "Invalid Syntax in Entity part of level file " << filename << "!" << std::endl;
                return false;
            }
            break;

        case sInKey:
            switch(c)
            {
            case '"':
                curState = sPastKey;
                break;
            default:
                curKey += c;
                break;
            }
            break;

        case sPastKey:
            switch(c)
            {
            case ' ':
            case '\t':
            case '\n':
                //ignore whitespaces
                break;
            case '"':
                curState = sInValue;
                curValue.clear();
                break;
            default:
                std::cerr << "Invalid Syntax in Entity part of level file " << filename << "!" << std::endl;
                return false;
            }
            break;

        case sInValue:
            switch(c)
            {
            case '"':
                curState = sInEntity;
                std::transform(curKey.begin(), curKey.end(), curKey.begin(), tolower);
                if(curKey == "classname")
                {
                    if(curEntity.classname.empty())
                    {
                        curEntity.classname = curValue;
                    }
                    else
                    {
                        std::cout<<"Warning: duplicate key \"classname\" in Entity in level file " << filename << "!" << std::endl;
                    }
                }
                else
                {
                    if(curEntity.properties.find(curKey) == curEntity.properties.end())
                    {
                        curEntity.properties[curKey] = curValue;
                    }
                    else
                    {
                        std::cout<<"Warning: duplicate key \"" << curKey << "\" in Entity in level file " << filename << "!" << std::endl;
                    }
                }
                break;
            default:
                curValue += c;
                break;
            }
            break;
        }
        std::string buf;

    }
}
