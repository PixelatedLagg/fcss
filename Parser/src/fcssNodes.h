#include <string>
#include <list>

enum _PositionMode { StickToScreen, FlowTopDown };


struct Point2D {
    int x;
    int y;
};


struct _Colour {
    int R;
    int G;
    int B;
};


struct _Thickness {
    double Left;
    double Right;
    double Top;
    double Bottom;
};


struct _Border {
    _Colour Colour;
    _Thickness Thickness;
};


struct _Shadow {
    Point2D Offset;
    _Colour Colour;
    _Thickness Thickness;
    double FadeDistance;
};


class Event {
    std::string Name;

    // TODO: Optional parameters to be passed
    int Call();
};


class Element {
    std::string Tag;

    Element *Parent;
    std::list<Element*> Children;
    std::string Id;
    std::string Class;

    std::list<Event*> Events;
    _PositionMode PositionMode;

    int Width;
    int Height;
    int InnerWidth;
    int InnerHeight;
    
    int ZIndex;
    Point2D TopLeft;
    Point2D BottomLeft;
    Point2D TopRight;
    Point2D BottomRight;
    Point2D InnerTopLeft;
    Point2D InnerBottomLeft;
    Point2D InnerTopRight;
    Point2D InnerBottomRight;
    Point2D Center;

    Point2D Origin; // Equals TopLeft coordinate

    int RoundCorners = 0;
    double Opacity = 1;

    _Colour Background;
    _Colour Foreground;
    _Border Border;
    _Shadow Shadow;

    Element(Element* Parent, std::string Tag, int Width, int Height, Point2D Origin);
    Element(Element* Parent, std::string Tag);

    void AddChild(Element* Child);
    void AddEvent(Event* _Event);

    void SetOrigin(Point2D Origin);

    void SetWidth(int NewWidth);
    void SetHeight(int NewHeight);
    void SetZIndex(int ZIndex);

    void SetInnerWidth(int InnerWidth);
    void SetInnerHeight(int InnerHeight);
};
