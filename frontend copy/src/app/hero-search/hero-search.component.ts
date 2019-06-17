import { Input,Component, OnInit,OnChanges,SimpleChanges } from '@angular/core';
import { Router }            from '@angular/router';
 
import { Observable }        from 'rxjs/Observable';
import { Subject }           from 'rxjs/Subject';
 
// Observable class extensions
import 'rxjs/add/observable/of';
 
// Observable operators
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/debounceTime';
import 'rxjs/add/operator/distinctUntilChanged';
 
import { HeroService } from '../hero.service';
import { Hero } from '../hero';

@Component({
  selector: 'app-hero-search',
  templateUrl: './hero-search.component.html',
  styleUrls: ['./hero-search.component.css']
})
export class HeroSearchComponent implements OnInit,OnChanges {

  heroes : Observable<Hero []>;
  private searchTerm = new Subject<string>();
  constructor(private heroService:HeroService,
              private route:Router) { }
  @Input() term: String;
  search(term:string):void{
    return this.searchTerm.next(term);
  }

  ngOnInit() {

    this.heroes = this.searchTerm
                        .debounceTime(300)
                        .distinctUntilChanged()
                        .switchMap(term=>term
                                    ? this.heroService.search(term)
                                    :Observable.of<Hero[]>([]))
                                    .catch(error=>{
                                      console.log(error);
                                      return Observable.of<Hero[]>([]);
                                    })


  }

goToDetail(hero:Hero):void{
  this.route.navigate(['/detail',hero.id]);
}
changeLog: string[] = [];
ngOnChanges(changes: SimpleChanges) {
  
  for (let propName in changes) {
    let chng = changes[propName];
    let cur  = JSON.stringify(chng.currentValue);
    let prev = JSON.stringify(chng.previousValue);
    this.changeLog.push(`${propName}: currentValue = ${cur}, previousValue = ${prev}`);
  }
}

}
