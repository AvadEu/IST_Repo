#!/bin/bash

echo "Jaki jest twój ulubiony system operacyjny?"
read os

if [[ "$os" == "Windows" || "$os" == "Mac" ]]; then
    echo "Ta, weź idź do wulkanizatora zmienić opony mózgowe hehe."
elif [[ "$os" == "Linux" ]]; then
    echo "Świetny wybór!"
else
    echo "Czy $os jest systemem operacyjnym?"
fi