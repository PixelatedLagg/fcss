#include <string>

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
}


struct _Border {
    _Colour Colour;
    _Thickness Thickness;
}


struct _Shadow {
    Point2D Offset;
    _Colour Colour;
    _Thickness Thickness;
    double FadeDistance;
}


class Event {
    std::string Name;

    // TODO: Optional parameters to be passed
    int Call();
}


class Element {
    std::string Tag;

    Element Parent;
    Element[] Children;
    std::string Id;
    std::string Class;

    Event[] Events;
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
}
