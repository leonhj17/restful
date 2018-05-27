/**
 * Created by Thinkpad on 2018/3/23.
 */
///////////////////////////////////////////////////////////////
//Datetime 格式化
// 对Date的扩展，将 Date 转化为指定格式的String
// 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符，
// 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字)
// 例子：
// (new Date()).Format("yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423
// (new Date()).Format("yyyy-M-d h:m:s.S")      ==> 2006-7-2 8:9:4.18
(function () {
Date.prototype.Format = function (fmt) { //author: meizz
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "h+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
};
})();


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
      t = new Date(d.time);
      tooltip.html(
          'KKS编号：'+d.sensorKks.sensorKks+'<br />'+
          '烟温：'+d.value+'℃'+'<br />'+
          '时间：'+t.Format('yyyy-MM-dd hh:mm:ss')+'<br />'
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
      t = new Date(d.time);
      tooltip.html(
          'KKS编号：'+d.sensorKks.sensorKks+'<br />'+
          '烟温：'+d.value+'℃'+'<br />'+
          '时间：'+t.Format('yyyy-MM-dd hh:mm:ss')+'<br />'
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

// 轨迹线界面，散点图
function trackPlot(svg, data) {
      var width = svg.attr('width'),
          height = svg.attr('height'),
          radius = Math.min(width, height) / 2 - 30;

      var distance = [];
      for (var i=0 ;i<data.length ;i++ ) {
          distance.push(data[i].distance)
      }
      var max = Math.max.apply(null, distance);
      if ( String(Math.floor(max)).length === 3 ) {
          max = Math.ceil(max/100)*100;
          console.log(max);
      }else if (String(Math.floor(max)).length === 2) {
          max = Math.ceil(max/10)*10;
          console.log(max);
      }else {
          console.log('****')
      }
      var angle = d3.scaleLinear()
      .domain([0, 360])
      .range([0, 2 * Math.PI]);
      var r = d3.scaleLinear()
      .domain([0, max])
      .range([0, radius]);
       //根据svg（宽度或高度）确定极坐标半径
      var opc = d3.scaleLinear()
          .domain([0,data.length])
          .range([1,0]);

      var svg = svg.append("g")
                .attr('class', 'center')
                .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
    //添加g元素，定位与svg中心点
      var gr = svg.append("g")
          .attr("class", "r axis")
          .selectAll("g")
          .data(r.ticks(10).slice(1))
          .enter().append("g");
    //gr.append("circle")
    // .attr('r', r); 与下面实现效果相同
    //用以根据r的极值，绘制极坐标环线
    gr.append("circle")
          .attr("r", function (d) {
              return r(d)
          });
    //绘制极坐标环线标识
    gr.append("text")
        .attr("y", function(d) { return -r(d)-4 ; })
        .attr("transform", "rotate(20)")
        .style("text-anchor", "middle")
        .text(function(d) { return d; });
    //在g.center元素下，添加g.a axis元素
      //继续添加g元素，并依次旋转-90 ~ 225°
      //原translate处理将中心定位到svg中心
      //rotate后，将坐标轴（x,y）也依次作相应角度旋转
    var ga = svg.append("g")
          .attr("class", "a axis")
          .selectAll("g")
          .data(d3.range(-90, 270, 45))
          .enter().append("g")
          .attr("transform", function(d) {
            return "rotate(" + d + ")";
        });
    //line依照各自坐标轴添加，为定义参数，x1,y1,y2默认为0
    ga.append("line")
          .attr("x2", radius);
    ga.append("text")
        .attr("x", radius + 6)
        .attr("dy", "0.35em")
        .style("text-anchor", function(d) { return d < 270 && d > 90 ? "end" : null; })
        .attr("transform", function(d) {
            return d < 270 && d > 90 ? "rotate(180 " + (radius+6) + ",0)" : null;
        })
        .text(function(d,i) { return i*45 + "°" });
      var i0 = d3.interpolateHsvLong(d3.hsv(120, 1, 0.65), d3.hsv(60, 1, 0.90)),
        i1 = d3.interpolateHsvLong(d3.hsv(60, 1, 0.90), d3.hsv(0, 1, 0.95)),
        interpolateTerrain = function(t) { return t < 0.5 ? i0(t * 2) : i1((t - 0.5) * 2); },
        color = d3.scaleSequential(interpolateTerrain).domain([0, 500]);
    //返回path，从原点出发，指向返回值
    var rline = d3.lineRadial()
          .angle(function(d) {
            return angle(d[0]);
          })
          .radius(function(d) {
            return r(d[1]);
          });

    svg.selectAll("point")
          .data(data)
          .enter()
          .append("circle")
          .attr("class", "point")
          .attr('id', function (d, i) {
              return i
          })
          .attr("transform", function(d) {
              //去除类数组元素第一个及最后一个元素；
            var coors = rline([[d.angle,d.distance]]).slice(1).slice(0, -1);
            return "translate(" + coors + ")"
          })
          .attr("r", 10)
          .attr('opacity', function(d,i) {
              return  opc(i)
          })
          .attr("fill", 'green')
          .on('mouseover',function (d) {
              $(this).attr('fill', 'yellow').attr('opacity', '0.8');
              t = new Date(d.time);
              tooltip.html(
                  '偏心距：'+d.distance+'<br />'+
                  '偏转角：'+d.angle+'°'+'<br />'+
                  '象限：第'+d.region+'象限'+'<br />'+
                  '时间：'+t.Format('yyyy-MM-dd hh:mm:ss')+'<br />'
              )
                  .style('left',(d3.event.pageX)+'px')
                  .style('top',(d3.event.pageY+20)+'px')
                  .style('opacity',1.0)
              })
          .on('mouseout',function (d, i) {
              $(this).attr('fill', 'green')
                  .attr('opacity', opc(i));
              tooltip.style('opacity',0.0)
          });
}
//////////////////////////////////////////////////////////
//等温线图legend 图例
function legendPlot(svg, uplimit, dnlimit, space) {
    var width = svg.attr('width');
    var height = svg.attr('height');

    var ldata = d3.range(uplimit, dnlimit, space);
    var lheight =height/ldata.length;
    // console.log(height, ldata);
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

//轨迹线legend 图例
function trackLegendPlot(svg, data) {
    var width = svg.attr('width');
    var height = svg.attr('height');

    var opc = d3.scaleLinear()
                 .domain([0,data.length])
                 .range([1,0]);

    var lheight =height/data.length;
    // console.log(height, ldata);
    var update = svg.selectAll('rect').data(data);

    var enter = update.enter();

    var exit = update.exit();

    update.attr('x', 0)
        .attr('y', function (d,i) {
            return i*lheight;
        })
        .attr('width', width)
        .attr('height', lheight)
        .style('fill', 'green')
        .attr('opacity', function (d, i) {
            console.log('i:'+i);
            console.log('opc:'+opc(i));
            return opc(i)
        })
        .attr('id', function (d, i) {
            return i
        })
        .on('mouseover',function (d) {
          $(this).attr('fill', 'green').attr('opacity', '0.8');
          var id = $(this).attr('id');

          var selected =$('.point#'+id);
          selected.attr('fill', 'yellow')
              .attr('opacity', 1);

          t = new Date(d.time);
          tooltip.html(
              // 'id:'+id+'<br />'+
              '时间：'+t.Format('yyyy-MM-dd hh:mm:ss')+'<br />'
          )
              .style('left',(d3.event.pageX +20)+'px')
              .style('top',(d3.event.pageY)+'px')
              .style('opacity',1.0)
          })
        .on('mouseout',function (d, i) {
              $(this).attr('fill', 'green')
                  .attr('opacity', opc(i));

              var id = $(this).attr('id');
              var selected =$('.point#'+id);
              selected.attr('fill', 'green')
                  .attr('opacity', opc(i));

              tooltip.style('opacity',0.0)
        });

    enter.append('rect')
        .attr('x', 0)
        .attr('y', function (d,i) {
            return i*lheight;
        })
        .attr('width', width)
        .attr('height', lheight)
        .style('fill', 'green')
        .attr('opacity', function (d, i) {
            console.log('i:'+i);
            console.log('opc:'+opc(i));
            return opc(i)
        })
        .attr('id', function (d, i) {
            return i
        })
        .on('mouseover',function (d) {
          $(this).attr('fill', 'green').attr('opacity', '0.8');
          var id = $(this).attr('id');

          var selected =$('.point#'+id);
          selected.attr('fill', 'yellow')
              .attr('opacity', 1);

          t = new Date(d.time);
          tooltip.html(
              // 'id:'+id+'<br />'+
              '时间：'+t.Format('yyyy-MM-dd hh:mm:ss')+'<br />'
          )
              .style('left',(d3.event.pageX +20)+'px')
              .style('top',(d3.event.pageY)+'px')
              .style('opacity',1.0)
          })
        .on('mouseout',function (d, i) {
              $(this).attr('fill', 'green')
                  .attr('opacity', opc(i));

              var id = $(this).attr('id');
              var selected =$('.point#'+id);
              selected.attr('fill', 'green')
                  .attr('opacity', opc(i));

              tooltip.style('opacity',0.0)
        });

    exit.remove();

}