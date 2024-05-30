#include <iostream>
#include <thread>
#include <chrono>

void afficherMessageAvecPause(const std::string& message, int pauseEnSecondes) {
    std::cout << message << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(pauseEnSecondes));
}

int main() {
    std::string messages[] = {
        "Bonjour",
        "Comment ça va ?",
        "Ca va bien ?",
    };

    int pauseEnSecondes = 2;

    for (const auto& message : messages) {
        afficherMessageAvecPause(message, pauseEnSecondes);
    }

    return 0;
}

