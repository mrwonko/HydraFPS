#include <SFML/Graphics.hpp>
#include <sixense.h>
#include <btBulletDynamicsCommon.h>
#include <iostream>
#include <cassert>

#include <LevelFormat.hpp> //temporary, to see if it compiles

// Making sure Sixense exits properly, even when exceptions happen. (Not sure about exit() though...)
class SixenseAutoExit
{
public:
    ~SixenseAutoExit()
    {
        assert(sixenseExit() == SIXENSE_SUCCESS);
    };
};

int main(int argc, const char** argv)
{
    if(sixenseInit() != SIXENSE_SUCCESS)
    {
        std::cerr<<"Could not init Sixense SDK!"<<std::endl;
        return 0;
    }
    SixenseAutoExit sixenseAutoExit;
    sf::RenderWindow window(sf::VideoMode(800, 600), "7dfps warmup: Hydra FPS");
    while(window.isOpen())
    {
        sf::Event ev;
        while(window.pollEvent(ev))
        {
            // Rendering
            window.clear();

            // Event Polling
            switch(ev.type)
            {
            case sf::Event::Closed:
                window.close();
                break;
            }
        }

        // Game Logic

        // Buffer Flip
        window.display();
    }
    return 0;
}
