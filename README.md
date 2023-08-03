# FCss - Functional CSS
FCss is a superset of the classic CSS language and aims to provide more functionality

## Example

```fcss
[#my_class].init {
    width = Screen.width * .90;

    if (this.last()) {
        border.bottom = border.bottom + 3;
    }    
}
```

## Features
Position mode | Description | Example
---|---|---
Pixels | The default position mode of an element. This enables the position of the element to be specified using the pixel coordinate system. | `position_mode = Position_mode.pixels;`
Sticky | This makes the element stick to the user's screen, still specified using the pixel coordinate system. | `position_mode = Position_mode.sticky;`
Top_Down | This makes the element render below the lowest element. Basically the same as traditional HTML/CSS. | `position_mode = Position_mode.top_down;`
