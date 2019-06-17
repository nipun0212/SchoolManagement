import { Component, OnInit } from '@angular/core';
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
export class HeroSearchComponent implements OnInit {

  heroes : Observable<Hero []>;
  private searchTerm = new Subject<string>();
  constructor(private heroService:HeroService,
              private route:Router) { }

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

}
