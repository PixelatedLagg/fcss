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
Compared to:
```css
#my_class
{
    width: 90%;
    margin-bottom: 10px; /* hope you know the exact value! */
}
#my_class_parent:not(:last-child)
{
    margin-bottom: 13px; /* this one too! */
}
```

## Features
Position mode | Description | Example
---|---|---
Pixels | The default position mode of an element. This enables the position of the element to be specified using the pixel coordinate system. | `position_mode = Position_mode.pixels;`
Sticky | This makes the element stick to the user's screen, still specified using the pixel coordinate system. | `position_mode = Position_mode.sticky;`
Top_Down | This makes the element render below the lowest element. Basically the same as traditional HTML/CSS. | `position_mode = Position_mode.top_down;`

### Variables

FCss enables the developer to easily create and manage variables with methods. Additionally, FCss features a garbage collector, so no need to manage variable memory.

Method | Description
---|---
`set(name, value)` | If a variable with `name` exists, set the value as `value`. If not, create a variable named `name` and set its value to `value`.
`get(name)` | If a variable with `name` exists, return its value. If not, return NULL.
