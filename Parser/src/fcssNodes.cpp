#include "fcssNodes.h"

namespace fcss::Parser {
    _Colour ColourFromHex(std::string HexString) {
        HexString = HexString.substr(1);
        if (HexString.length() == 3) {
            HexString = HexString + HexString;
        }

        int R, G, B;
        std::sscanf(HexString.c_str(), "%02x%02x%02x", &R, &G, &B);

        _Colour Colour;
        Colour.R = R;
        Colour.G = G;
        Colour.B = B;
        Colour.A = 1;

        return Colour;
    }

    Element::Element(Element* Parent, std::string Tag, int Width, int Height, Point2D Origin) {
        // Other elements can be manually set
        this->Parent = Parent;
        this->Tag = Tag;
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

    Element::Element(Element* Parent, std::string Tag) {
        this->Parent = Parent;
        this->Tag = Tag;
    }

    void Element::AddChild(Element* Child) {
        Child->Parent = this;
        Children.push_back(Child);
    }

    void Element::AddEvent(Event* _Event) {
        Events.push_back(_Event);
    }

    void Element::SetOrigin(Point2D Origin) {
        this->Origin = Origin;
        this->TopLeft = Origin;

        this->SetHeight(this->Height);
        this->SetWidth(this->Width);
    }

    void Element::SetPositionMode(_PositionMode PositionMode) {
        this->PositionMode = PositionMode;
    }

    void Element::SetHeight(int Height) {
        this->Height = Height;
        this->BottomLeft.y = this->Origin.y + Height;
        this->BottomRight.y = this->Origin.y + Height;

        this->SetInnerHeight(this->InnerHeight);
    }

    void Element::SetWidth(int Width) {
        this->Width = Width;
        this->TopRight.x = this->Origin.x + Width;
        this->BottomRight.x = this->Origin.x + Width;

        this->SetInnerWidth(this->InnerWidth);
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

    void Element::SetBackground(int R, int G, int B) {
        _Colour Colour;
        Colour.R = R;
        Colour.G = G;
        Colour.B = B;
        Colour.A = 1;

        this->Background = Colour;
    }

    void Element::SetBackground(int R, int G, int B, double A) {
        _Colour Colour;
        Colour.R = R;
        Colour.G = G;
        Colour.B = B;
        Colour.A = A;

        this->Background = Colour;
    }

    void Element::SetBackground(_Colour Colour) {
        this->Background = Colour;
    }

    void Element::SetBackground(std::string HexString) {
        _Colour Colour = ColourFromHex(HexString);
        this->Foreground = Colour;
    }

    void Element::SetForeground(int R, int G, int B) {
        _Colour Colour;
        Colour.R = R;
        Colour.G = G;
        Colour.B = B;
        Colour.A = 1;

        this->Foreground = Colour;
    }

    void Element::SetForeground(int R, int G, int B, double A) {
        _Colour Colour;
        Colour.R = R;
        Colour.G = G;
        Colour.B = B;
        Colour.A = A;

        this->Foreground = Colour;
    }

    void Element::SetForeground(_Colour Colour) {
        this->Background = Colour;
    }

    void Element::SetForeground(std::string HexString) {
        _Colour Colour = ColourFromHex(HexString);
        this->Foreground = Colour;
    }    
}
