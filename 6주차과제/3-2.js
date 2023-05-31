function getDivisiors(x){
    var yaksu=[];
    for(var i=1; i<Math.sqrt(x); i++)
    {
       if(x%i===0)
       {
         yaksu.concat([i, (x/i)]);
       }
    }
    return yaksu.sort((first, second) => first - second);
}

const ellipse={
    width:10,
    height:5,
    getArea: function(){return Math.PI*width*height},
    getPerimeter: function(){return Math.PI*2*sqrt((width*width+height*height)/2)},
    getEccentricity: function(){return sqrt(1-(height/width)*(height/width))} 
};