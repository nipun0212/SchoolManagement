import { Component, OnInit } from '@angular/core';
import {Hero} from '../hero';
import {HeroService} from '../hero.service'
import {ActivatedRoute,Router} from '@angular/router';
@Component({
  selector: 'app-heroes',
  templateUrl: './heroes.component.html',
  styleUrls: ['./heroes.component.css'],
  providers:[HeroService]
})
export class HeroesComponent implements OnInit {
  constructor(private heroService:HeroService,private route:Router){}
  heroes :Hero[];
  title = 'Hero Details';
  selectedHero : Hero;
  
  getHeroes():void{
  this.heroService.getHeroesSlowly().then(heroes =>this.heroes=heroes);
  }
  onSelect(hero:Hero):void{
    this.selectedHero = hero;
  }
  goToDetail():void{
    this.route.navigate(['/detail',this.selectedHero.id]);
  }
ngOnInit():void{
  this.getHeroes();
}

add(name:string):void{
name = name.trim();
if(!name){return}
this.heroService.create(name).then(hero=>{
  this.heroes.push(hero);
  this.selectedHero = null;
});
}

delete(hero:Hero):void{
  this.heroService.delete(hero.id)
  .then(()=>{
    this.heroes = this.heroes.filter(h=>h!=hero);
    if (this.selectedHero === hero){
      this.selectedHero = null;
    }})
  }
}
