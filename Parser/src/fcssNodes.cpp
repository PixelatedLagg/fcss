#include "fcssNodes.h"

Element::Element(Element Parent, int Width, int Height, Point2D Origin) {
    // Other elements can be manually set
    this->Parent = Parent;
    this->Width = Width;
    this->Height = Height;
    this->Origin = Origin;

    this->TopLeft = Origin;

    this->BottomLeft.x = Origin.x;
    this->BottomLeft.y = Origin.y + Height;

    this->TopRight.x = Origin.x + Width;
    this->TopRight.y = Origin.y;

    this->BottomRight.x = Origin.x + Width;
    this->BottomRight.y = Origin.y + Height;

    this->Center.x = (Origin.x + Width) / 2;
    this->Center.y = (Origin.y + Height) / 2;
}

void Element::AddChild(Element Child) {
    Child.Parent = this;
    Children.push_back(Child);
}

void Element::SetHeight(int Height) {
    this->Height = Height;

    this->BottomLeft.y = this->Origin.y + Height;
    this->BottomRight.y = this->Origin.y + Height 
}

void Element::SetWidth(int Width) {
    this->Width = Width;
    this->TopRight.x = this->Origin.x + Width;
    this->BottomRight.x = this->Origin.x + Width;
}
