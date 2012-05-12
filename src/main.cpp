#include <SFML/Graphics.hpp>

int main(int argc, const char** argv)
{
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

            // Game Logic

            // Buffer Flip
            window.display();
        }
    }
    return 0;
}
