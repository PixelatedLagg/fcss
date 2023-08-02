#include "fcssNodes.h"

Element::Element(Element* Parent, int Width, int Height, Point2D Origin) {
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

void Element::AddChild(Element* Child) {
    Child->Parent = this;
    Children.push_back(Child);
}

void Element::AddEvent(Event* _Event) {
    Events.push_back(_Event);
}

void Element::SetHeight(int Height) {
    this->Height = Height;
    this->BottomLeft.y = this->Origin.y + Height;
    this->BottomRight.y = this->Origin.y + Height;
}

void Element::SetWidth(int Width) {
    this->Width = Width;
    this->TopRight.x = this->Origin.x + Width;
    this->BottomRight.x = this->Origin.x + Width;
}

void Element::SetZIndex(int ZIndex) {
    this->ZIndex = ZIndex;
}

void Element::SetInnerWidth(int InnerWidth) {
    this->InnerWidth = InnerWidth;

    this->InnerTopLeft.x = this->Origin.x + InnerWidth;
    this->InnerTopRight.x = this->TopRight.x - InnerWidth;

    this->InnerBottomLeft.x = this->Origin.x + InnerWidth;
    this->InnerBottomRight.x = this->BottomRight.x - InnerWidth;
}

void Element::SetInnerHeight(int InnerHeight) {
    this->InnerHeight = InnerHeight;

    this->InnerTopLeft.y = this->Origin.y + InnerHeight;
    this->InnerTopRight.y = this->Origin.y + InnerHeight;

    this->InnerBottomLeft.y = this->BottomLeft.y - InnerHeight;
    this->InnerBottomRight.y = this->BottomRight.y - InnerHeight;
}
