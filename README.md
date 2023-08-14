# FCSS - Functional CSS
FCSS is a superset of the classic CSS language and aims to provide more functionality. *Disclaimer: All FCSS RFC styling is taken from www.rfc-editor.org*

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

FCSS enables the developer to easily create and manage variables with methods. Additionally, FCSS features a garbage collector, so no need to manage variable memory.

Method | Description
---|---
`set(name, value)` | If a variable with `name` exists, set the value as `value`. If not, create a variable named `name` and set its value to `value`.
`get(name)` | If a variable with `name` exists, return its value. If not, return NULL.

### Special Operators

On top of having the traditional arithmetic and comparison operators, FCSS also employs the following:

Operator | Description
---|---
`value^` | Round `value` to the nearest whole number (rounding up).
`value_` | Round `value` to the nearest whole number (rounding down).

### Selectors

Instead of the traditional CSS selectors and operators, FCSS uses a unique system akin to array indexing to select certain elements. Below are a few examples:

CSS:
```css
#someID { }

#someID + .someClassFollowingSomeID { }

.someClass.anotherClass { }

.thisClass > .followedByThisClass { }
```

FCSS:
```fcss
[#someID].init { }

[#someID][.someClassFollowingSomeID].init { }

[.someClass && .anotherClass].init { }

[.thisClass][.followedByThisClass].init { }
```

Here are some things CSS selectors can't do:

```fcss
[.someClass || #anotherID].init { } //select elements where class == someClass or id == anotherID

[!(.notThisClass)].init { } //select elements where class != notThisClass
```

Additionally, all selectors are stackable - including the wildcard selector `*`.

### Conditionals

Unlike CSS, FCSS features conditionals. The typical `if`, `else`, `if else`, and `switch` statements are included. With the `switch` in particular, the syntax is as follows:

```fcss
switch (value)
{
    case constValue:
    {
        //value == constValue
    }
    case
    {
        //value != any case
    }
}
```

## Implementing in Browsers

Obviously, FCSS means nothing without a browser to render it. The FCSS compiler will run through all dependencies and return a JSON file of all the relevant styling information, along with any dynamic instructions.

Sample FCSS:
```fcss
[.class || .other-class || .my_class || .important-class].init { }
```

Output JSON:
```json
{
    "Selector": {
        "Paths": [
            {
                "Or": {
                    "left": {
                        "Class": "class"
                    },
                    "right": {
                        "Or": {
                            "left": {
                                "Class": "other-class"
                            },
                            "right": {
                                "Or": {
                                    "left": {
                                        "Class": "my_class"
                                    },
                                    "right": {
                                        "Class": "important-class"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        ],
        "Instructions": [],
        "Event": "init"
    }
}
```
