import {Directive, ElementRef} from '@angular/core';

@Directive({selector:'[highlight]'})

export class HighlightDirective {
    constructor(e1:ElementRef){
        e1.nativeElement.style.backgroundColor = "gold";
        console.log(
            `* Approot highlight is called for ${e1.nativeElement.tagName}`);
    }
}