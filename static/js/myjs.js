/**
 * Created by Thinkpad on 2018/3/23.
 */
///////////////////////////////////////////////////////////////
//右侧工具条
    $('#hide').click(function () {
     $('#test').animate({width: 'toggle'}, 'fast')
    });
    //工具条栅格选项
  $("input:checkbox[name=xgrid]").click(function () {
      var xgrid = $(this).is(':checked');
      if (xgrid) {
          $('.xgrid').attr('opacity', '1');
      }else {
          $('.xgrid').attr('opacity', '0');
      }
  });

  $("input:checkbox[name=ygrid]").click(function () {
      var ygrid = $(this).is(':checked');
      if (ygrid) {
          $('.ygrid').attr('opacity', '1');
      }else {
          $('.ygrid').attr('opacity', '0');
      }
  });
/////////////////////////////////////////////////////////////////
//左侧导航条
    $('.navbar-toggler').click(function () {
     $('#sidebar-left').animate({width: 'toggle'}, 'fast');
     $('#mask').animate({opacity: 'toggle'}, 'fast');
    });

/////////////////////////////////////////////////////////////////
//现场值界面，散点图
function point(svg, json_data) {
  var width = svg.attr("width");
  var height = svg.attr("height");
  var padding = {'left': 55,'right': 30,'top':30, 'bottom': 30};
    //栅格线
  var xtick = [0, 3600, 7200, 10440, 14280, 17880,21480];
  var ytick = [0, 3280, 6280, 10740, 12200, 15200, 18200, 21480];

  var x_tick_scale = d3.scaleLinear()
      .domain([0, 21480])
      .range([padding.left, width-padding.right]);

  var y_tick_scale = d3.scaleLinear()
      .domain([0, 21480])
      .range([padding.top, height-padding.bottom]);

  var xgird = svgPoint.selectAll('.xgrid')
      .data(xtick)
      .enter()
      .append("g")
      .attr('class', 'xgrid');

  xgird.append('line')
      .attr('x1', function (d) {
          return x_tick_scale(d)
      })
      .attr('x2', function (d) {
          return x_tick_scale(d)
      })
      .attr('y1', y_tick_scale(0))
      .attr('y2', y_tick_scale(21480));

  var ygird = svgPoint.selectAll('.ygrid')
      .data(ytick)
      .enter()
      .append("g")
      .attr('class', 'ygrid');

  ygird.append('line')
      .attr('y1', function (d) {
          return y_tick_scale(d)
      })
      .attr('y2', function (d) {
          return y_tick_scale(d)
      })
      .attr('x1', x_tick_scale(0))
      .attr('x2', x_tick_scale(21480));

    //坐标轴
  var xaxis = d3.axisBottom(x_tick_scale)
      .tickValues(xtick);
  var yaxis = d3.axisRight(y_tick_scale)
      .tickValues(ytick);
      svg.append('g')
          .attr('class','xaxis')
          .call(xaxis);
      svg.append('g')
          .attr('class', 'yaxis')
          .call(yaxis);


    //散点
  var xscale = d3.scaleLinear()
      .domain([0, 21480])
      .range([padding.left, width-padding.right]);

  var yscale = d3.scaleLinear()
      .domain([0, 21480])
      .range([padding.top, height-padding.bottom]);

  var update = svg.selectAll('circle')
      .data(json_data);

  var enter = update.enter();

  var exit = update.exit();

  update
    .attr('cx',function (d,i) {
        return xscale(d.sensorKks.x)
    })
    .attr('cy',function (d,i) {
        return yscale(d.sensorKks.y)
    })
    .attr('r',10)
    .attr('fill',function (d) {
        return color(d.value)
    })
  .on('mouseover',function (d) {
      $(this).attr('fill', 'yellow').attr('opacity', '0.8');
      tooltip.html(
          'KKS编号：'+d.sensorKks.sensorKks+'<br />'+
          '烟温：'+d.value+'℃'+'<br />'+
          '时间：'+d.time+'℃'+'<br />'
      )
          .style('left',(d3.event.pageX)+'px')
          .style('top',(d3.event.pageY+20)+'px')
          .style('opacity',1.0)
      })
      .on('mouseout',function (d) {
          $(this).attr('fill', color(d.value)).attr('opacity', '1');
          tooltip.style('opacity',0.0)
      });


  enter
      .append('a')
      .attr('xlink:href', function (d, i) {
          return '/highcharts/'+d.sensorKks.id
      })
      .append('circle')
    .attr('cx',function (d,i) {
        return xscale(d.sensorKks.x)
    })
    .attr('cy',function (d,i) {
        return yscale(d.sensorKks.y)
    })
    .attr('r',10)
    .attr('fill',function (d) {
        return color(d.value)
    })
    .on('mouseover',function (d) {
      $(this).attr('fill', 'yellow').attr('opacity', '0.8');
      tooltip.html(
          'KKS编号：'+d.sensorKks.sensorKks+'<br />'+
          '烟温：'+d.value+'℃'+'<br />'+
          '时间：'+d.time+'<br />'
      )
          .style('left',(d3.event.pageX)+'px')
          .style('top',(d3.event.pageY+20)+'px')
          .style('opacity',1.0)
      })
      .on('mouseout',function (d) {
          $(this).attr('fill', color(d.value)).attr('opacity', '1');
          tooltip.style('opacity',0.0)
      });

  exit.remove();

}

//////////////////////////////////////////////////////////
//等温线图legend 图例
function legendPlot(svg, uplimit, dnlimit, space) {
    var width = svg.attr('width');
    var height = svg.attr('height');

    var ldata = d3.range(uplimit, dnlimit, space);
    var lheight =height/ldata.length;
    console.log(height, ldata);
    var update = svg.selectAll('rect').data(ldata);

    var enter = update.enter();

    var exit = update.exit();

    update.attr('x', 0)
        .attr('y', function (d,i) {
            return i*lheight;
        })
        .attr('width', width)
        .attr('height', height)
        .style('fill',function (d) {
            return color(d)
        });

    enter.append('rect')
        .attr('x', 0)
        .attr('y', function (d,i) {
            return i*lheight;
        })
        .attr('width', width)
        .attr('height', height)
        .style('fill',function (d) {
            return color(d)
        });

    exit.remove();

}

//现场值散点图legend 图例
function scatterLegendPlot(svg, uplimit, dnlimit, space) {
    var width = svg.attr('width');
    var height = svg.attr('height');

    var ldata = d3.range(uplimit, dnlimit, space);
    var lheight =height/ldata.length;

    var update = svg.selectAll('.scatter_legend').data(ldata);

    var enter = update.enter();

    var exit = update.exit();

    update.attr('class', 'scatter_legend')
        .attr('cx', 50)
        .attr('cy', function (d,i) {
            return (i+0.5)*lheight;
        })
        .attr('r', 10)
        .style('fill',function (d) {
            return color(d)
        });

    enter.append('circle')
        .attr('class', 'scatter_legend')
        .attr('cx', 50)
        .attr('cy', function (d,i) {
            return (i+0.5)*lheight;
        })
        .attr('r', 10)
        .style('fill',function (d) {
            return color(d)
        });

    exit.remove();

}