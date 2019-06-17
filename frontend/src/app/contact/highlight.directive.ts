import {Directive, ElementRef} from '@angular/core';

@Directive({selector:'[highlight],input'})

export class HighlightDirective {
    constructor(e1:ElementRef){
        e1.nativeElement.style.backgroundColor = "powderblue";
        console.log(
            `* Approot highlight is called for ${e1.nativeElement.tagName}`);
    }
}