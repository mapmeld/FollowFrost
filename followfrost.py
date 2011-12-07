import cgi, logging, random
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import memcache, images
from google.appengine.api.urlfetch import fetch, GET, POST

class Home(webapp.RequestHandler):
  def get(self):
	self.response.out.write('''<!DOCTYPE html>
<html>
	<head>
		<title>MoJo FollowFrost</title>
		<script type="text/javascript" src="JQUERY"></script>
		<script type="text/javascript" src="POPCORN (jQuery-independent, I assume)"></script>
		<script type="text/javascript">
		</script>
		<style type="text/css">
html, body{
	font-family:tahoma;
}
div.nav{
	background-color:black;
	padding:4px;
	color:white;
	width:70%;
	margin-left:9%;
	padding-left:4%;
}
table{
	width:74%;
	margin-left:9%;
	margin-right:9%;
	padding-left:4%;
	padding-right:4%;
	padding-top:20px;
	padding-bottom:20px;
	background-color:#4488ff;
}
span.navitem{
	display:inline:
	margin-left:15px;
	margin-right:15px;
	padding:4px;
	background-color:black;
	color:white;
	cursor:pointer;
	text-align:center;
}
span.navitem:hover{
	color:orange;
}
span.navitem a{
	text-decoration:none;
	color:white;
}
span.navitem a:hover{
	color:orange;
}
span.selectitem{
	color:orange;
}
button{
	cursor:pointer;
}
button.watch{
	border:none;
	background-color:darkgreen;
	color:white;
}
li{
	padding:12px;
}
li.response{
	list-style-type:circle;
	margin-left:50px;
}
		</style>
	</head>
	<body>
		<h1 style="margin-left:14%;">Welcome to FollowFrost</h1>
		<div class="nav"><nav>
			<span class="navitem selectitem">Intro</span>|
			<span class="navitem">Top Interviews</span>|
			<span class="navitem">Breaking News</span>|
			<span class="navitem">
				<a href="/login">Sign In</a>
			</span>
		</nav></div>
		<table>
			<tr>
				<td>
					<div style="border:1px solid black;background-color:white;padding:5px;">
						<b>What's this all about?</b>
						<br/>
						<p>FollowFrost is an open project to extend online video interviews for better engagement between interviewees, journalists, and commenters.
						<br/><br/>
						Ask follow-up questions, find great people to follow on Twitter, and easily narrow video content to the exact frames that you want.</p>
					</div>
				</td>
				<td>
					<h3 class="heading">Get started</h3>
					<ul>
						<li>Watch an interview</li>
						<li>Ask a question, get a video response</li>
						<li>Find people doing interesting work</li>
						<li>Start your own Q&amp;A</li>
					</ul>
				</td>
			</tr>
		</table>
		<div class="footer" style="margin-left:10%;">
			Powered by the open web technology <a href="http://popcornjs.org" target="_blank">Popcorn.js</a>
			<br/><br/>
			Developed for the Knight-Mozilla Learning Lab and TimesOpen Hack Day 2011
		</div>
	</body>
</html>''')

class View(webapp.RequestHandler):
  def get(self):
	interview = Interview.get_by_id(long(self.request.get('id')))
	if(interview is None):
		#self.redirect('/followfrost')
		#return
		interview = Interview()
		interview.title = "Make: Live - Maker Faire Detroit"
		interview.videos = ["youtube:z22AanAuKJQ"]
		interview.description = "Interviews with several makers and follow-ups"
		interview.tags = []
		interview.questions = []
		interview.answers = []
		interview.put()
	if(interview.description is None):
		interview.description = 'no description'
		interview.put()
	self.response.out.write('''<!DOCTYPE html>
<html>
	<head>
		<title>MoJo FollowFrost</title>
		<!-- <script type="text/javascript" src="http://mapmeld.appspot.com/popcorn.min.js"></script> -->
		<script type="text/javascript" src="http://popcornjs.org/code/dist/popcorn-complete.min.js"></script>
		<script type="text/javascript">
var myPopcorn, currentVideo;
var allVideos = ["''' + '","'.join(interview.videos) + '''"];
function initVid(vdex){
	var loadVid = allVideos[vdex];
	currentVideo = vdex;
	if(loadVid.split(":")[0] == "ogg"){
		var vidEl = document.createElement('video');
		vidEl.style.width = "100%";
		vidEl.style.height = "100%";
		vidEl.src = loadVid.split(":")[1];
		vidEl.id = "popcornsite_vid";
		$("popcornsite").addChild(vidEl);
		myPopcorn = Popcorn('#popcornsite_vid');
	}
	else if(loadVid.split(":")[0] == "youtube"){
		myPopcorn = Popcorn.youtube( 'popcornsite', 'http://www.youtube.com/watch?v=' + loadVid.split(":")[1], { width: 480 } );
	}
	else if(loadVid.split(":")[0] == "vimeo"){
		myPopcorn = Popcorn.vimeo( 'popcornsite', 'http://www.vimeo.com' + loadVid.split(":")[1], {width: 480 } );
	}
	myPopcorn.play();
	connectPlugins();
}
function connectPlugins(){\n''')
	if(interview.plugins == []):
		self.response.out.write('''
	myPopcorn
	.tagthisperson({
		start:50,
		end:70,
		person:'Matt Richardson, co-host of Make: Live',
		image:'http://0.gravatar.com/avatar/8090f2411aa56ec040114f39fa56922e?s=212&d=http%3A%2F%2F0.gravatar.com%2Favatar%2Fad516503a11cd5ca435acc9bb6523536%3Fs%3D50&r=G',
		href:'http://twitter.com/mattrichardson',
		target: 'tagdiv'
	})
	.twitter({
		start:50,
		end:70,
		title:'Follow on Twitter',
		src:'@MattRichardson',
		target:'twitterdiv'
	})
	.tagthisperson({
		start:20,
		end:50,
		person:'Becky Stern, co-host of Make: Live',
		image:'http://sternlab.org/wp-content/uploads/2011/03/Screen-shot-2011-03-17-at-9.45.15-AM.png',
		href:'http://twitter.com/bekathwia',
		target: 'tagdiv'
	})
	.twitter({
		start:20,
		end:50,
		title:'Follow on Twitter',
		src:'@bekathwia',
		target:'twitterdiv'
	})
	.twitter({
		start:0,
		end:25,
		title:'Follow on Twitter',
		src:'@Makemagazine',
		target:'twitterdiv'
	})
	.tagthisperson({
		start:70,
		end:203,
		person:'Dale Dougherty, creator of Maker Faire (photo CC-BY James Duncan Davidson)',
		image:'http://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Etech05_Dale.jpg/220px-Etech05_Dale.jpg',
		href:'http://twitter.com/dalepd',
		target: 'tagdiv'
	})
	.twitter({
		start:80,
		end:203,
		title:'Follow on Twitter',
		src:'@dalepd',
		target:'twitterdiv'
	})
	.tagthisperson({
		start:203,
		end:273,
		person:'Theatre Bizarre, illegal playwrights',
		image:'http://blog.makezine.com/wp-content/uploads/2011/07/theatre-bizarre-opener.jpg',
		href:'http://theatrebizarre.com/',
		target: 'tagdiv'
	})
	.twitter({
		start:203,
		end:273,
		title:'Follow on Twitter',
		src:'@theatrebizarre',
		target:'twitterdiv'
	})
	.tagthisperson({
		start:273,
		end:597,
		person:'Gon-KiRin',
		image:'http://a3.sphotos.ak.fbcdn.net/hphotos-ak-snc6/262699_205784022800404_126929984019142_590200_235224_n.jpg',
		href:'http://www.facebook.com/gonkirin',
		target: 'tagdiv'
	})
	.twitter({
		start:273,
		end:597,
		title:'Follow on Twitter',
		src:'@gonkirin',
		target:'twitterdiv'
	})
	.tagthisperson({
		start:597,
		end:1025,
		person:'William Gurstelle, author of Practical Pyromaniac',
		image:'http://www.williamgurstelle.com/images/index_image.jpg',
		href:'http://www.williamgurstelle.com/',
		target: 'tagdiv'
	})
	.twitter({
		start:597,
		end:1025,
		title:'Follow on Twitter',
		src:'@wmgurst',
		target:'twitterdiv'
	})
	.tagthisperson({
		start:1025,
		end:1121,
		person:'Russ Wolfe, i3detroit',
		image:'http://www.i3detroit.com/wp-content/uploads/2011/07/5918958890_321588bce9_z-300x225.jpg',
		href:'http://www.i3detroit.com/',
		target: 'tagdiv'
	})
	.twitter({
		start:1025,
		end:1121,
		title:'Follow on Twitter',
		src:'@remakedetroit',
		target:'twitterdiv'
	})
	.tagthisperson({
		start:1121,
		end:1320,
		person:'Jim Burke, PowerRacingSeries.org',
		image:'http://www.powerracingseries.org/images/shell/groupphoto.jpg',
		href:'http://www.powerracingseries.org/',
		target: 'tagdiv'
	})
	.twitter({
		start:1121,
		end:1320,
		title:'Follow on Twitter',
		src:'@ppprs',
		target:'twitterdiv'
	})
	.tagthisperson({
		start:1320,
		end:1384,
		person:'Bre Pettis, founder of MakerBot',
		image:'http://www.brepettis.com/storage/layout/home-left-banner.jpg',
		href:'http://www.brepettis.com/',
		target: 'tagdiv'
	})
	.twitter({
		start:1320,
		end:1384,
		title:'Follow on Twitter',
		src:'@bre',
		target:'twitterdiv'
	})
	.tagthisperson({
		start:1384,
		end:1484,
		person:'Jim Burke, PowerRacingSeries.org',
		image:'http://www.powerracingseries.org/images/shell/groupphoto.jpg',
		href:'http://www.powerracingseries.org/',
		target: 'tagdiv'
	})
	.twitter({
		start:1384,
		end:1484,
		title:'Follow on Twitter',
		src:'@ppprs',
		target:'twitterdiv'
	})
	.twitter({
		start:1484,
		end:1568,
		title:'Follow on Twitter',
		src:'@digikey',
		target:'twitterdiv'
	})
	.twitter({
		start:1568,
		end:2116,
		title:'Follow on Twitter',
		src:'@backyardbrains',
		target:'twitterdiv'
	})
	.tagthisperson({
		start:1568,
		end:2116,
		person:'Greg Gage, BackyardBrains',
		image:'http://www.backyardbrains.com/images/SpikerBoxBurntOrange_sm.png',
		href:'http://www.backyardbrains.com/Home.aspx',
		target: 'tagdiv'
	});\n''')
	else:
		for video in interview.videos:
			self.response.out.write('	if(allVideos[currentVideo] == "' + video + '"){\n')
			pluginChain = ''
			for plugindata in interview.plugins:
				plugin = plugindata.split(',')
				if(plugin[0] == video):
					if(plugin[1] == 'twitter'):
						pluginChain = pluginChain + '''		.twitter({
			start:''' + plugin[2] + ''',
			end:''' + plugin[3] + ''',
			src:"''' + plugin[4] + '''",
			title:'Follow on Twitter',
			target:'twitterdiv'
		})'''
					elif(plugin[1] == 'tagthisperson'):
						pluginChain = pluginChain + '''		.tagthisperson({
			start:''' + plugin[2] + ''',
			end:''' + plugin[3] + ''',
			person:"''' + plugin[4] + '''",
			image:"''' + plugin[5] + '''",
			href:"''' + plugin[6] + '''",
			target:'tagdiv'
		})'''
				else:
					# breaking here because we assume plugins are sorted VID0,VID0,VID1,VID1,VID2
					break
			if(pluginChain != ''):
				self.response.out.write('		myPopcorn' + pluginChain + ';\n')
			self.response.out.write('	}\n')
	self.response.out.write('''}
function init(){
	initVid(0);
	myPopcorn.listen("pause", function(){
		if(window.history){
			if(window.history.pushState){
				 window.history.pushState({state:myPopcorn.currentTime()},'',"view?id=''' + str(interview.key().id()) + '''&t=" + myPopcorn.currentTime());
			}
		}
	});	
	if(gup("t")){
		if(gup("t") != ""){
			myPopcorn.currentTime(1*gup("t"));
		}
	}
	myPopcorn.listen("end", function(){
		if(allVideos.length < currentVideo+1){
			initVid(currentVideo+1);
		}
	});
}
function gup(nm){nm=nm.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");var rxS="[\\?&]"+nm+"=([^&#]*)";var rx=new RegExp(rxS);var rs=rx.exec(window.location.href);if(!rs){return null;}else{return rs[1];}}
function jumpTo(evt){
	var time = evt.offsetX / 478 * myPopcorn.duration();
	myPopcorn.currentTime(time);
}
		</script>
		<style type="text/css">
html, body{
	font-family:tahoma;
}
div.nav{
	background-color:black;
	padding:4px;
	color:white;
	width:70%;
	margin-left:9%;
	padding-left:4%;
}
table{
	width:74%;
	margin-left:9%;
	margin-right:9%;
	padding-left:4%;
	padding-right:4%;
	padding-top:20px;
	padding-bottom:20px;
	background-color:#4488ff;
}
span.navitem{
	display:inline:
	margin-left:15px;
	margin-right:15px;
	padding:4px;
	background-color:black;
	color:white;
	cursor:pointer;
	text-align:center;
}
span.navitem:hover{
	color:orange;
}
span.navitem a{
	text-decoration:none;
	color:white;
}
span.navitem a:hover{
	color:orange;
}
span.selectitem{
	color:orange;
}
button{
	cursor:pointer;
}
button.watch{
	border:none;
	background-color:darkgreen;
	color:white;
}
li{
	padding:12px;
}
li.response{
	list-style-type:circle;
	margin-left:50px;
}
div.commenting{
	background:#2989d8; /* Old browsers */
	background:-moz-linear-gradient(top, #2989d8 0%, #2580d0 50%, #207cca 51%, #7db9e8 100%); /* FF3.6+ */
	background:-webkit-gradient(linear, left top, left bottom, color-stop(0%,#2989d8), color-stop(50%,#2580d0), color-stop(51%,#207cca), color-stop(100%,#7db9e8)); /* Chrome,Safari4+ */
	background:-webkit-linear-gradient(top, #2989d8 0%,#2580d0 50%,#207cca 51%,#7db9e8 100%); /* Chrome10+,Safari5.1+ */
	background:-o-linear-gradient(top, #2989d8 0%,#2580d0 50%,#207cca 51%,#7db9e8 100%); /* Opera11.10+ */
	background:-ms-linear-gradient(top, #2989d8 0%,#2580d0 50%,#207cca 51%,#7db9e8 100%); /* IE10+ */
	filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#2989d8', endColorstr='#7db9e8',GradientType=0 ); /* IE6-9 */
	background: linear-gradient(top, #2989d8 0%,#2580d0 50%,#207cca 51%,#7db9e8 100%); /* W3C */
}
img{
	max-height:220px;
	max-width:100%;
}
#tagdiv img{
	display:block;
}
.boxy{
	-moz-box-shadow: 5px 8px 15px #444444;
	-webkit-box-shadow: 5px 8px 15px #444444;
	box-shadow: 5px 8px 15px #444444;
}
.twtr-hd{
	background-color:white;
}
.twtr-doc[style]{
	width:100% !important;
}
		</style>
	</head>
	<body onload="init();">
		<h1 style="margin-left:14%;">FollowFrost</h1>
		<div class="nav"><nav>
			<span class="navitem selectitem">Interview</span>|
			<span class="navitem">Coverage</span>|
			<span class="navitem">
				<a href="/login">Sign In</a>
			</span>
		</nav></div>
		<table>
			<tr>
				<td>
					<h3 class="heading">''' + cgi.escape(interview.title) + '''</h3>
					<div>
						<!--<div id="videooverlay" style="padding-top:15px;padding-left:35px;max-width:480px;position:absolute;background:transparent;color:#fff;">Semitransparent Text</div>-->
						<div id="popcornsite" width="480" height="360" style="padding:15px 15px 15px 15px;border:3px solid black;background-color:white;margin-right:25px;margin-bottom:-60px;" src="''' + interview.videos[0] + '''">
						</div>
						<img style="display:inline;margin-left:19px;margin-top:-14px" onclick="jumpTo(event)" src="http://mapmeld.appspot.com/makerfairetrack-600.png" width="560" style="margin-top:-200px;margin-left:19px;" height="30">
					</div>
					<div style="height:140px;">
					&nbsp;
					</div>
				</td>
				<td>
					<h3 class="heading">You're watching</h3>
					<div>
						<div id="tagdiv" class="boxy" style="max-width:100%;overflow:none;background-color:white;padding-bottom:4px;"></div>
						<br/>
						<div id="twitterdiv" class="boxy" style="max-width:100%;max-height:300px;overflow:none;background-color:#ddddff;"></div>
					</div>
				</td>
			</tr>
		</table>
		<div class="commenting" style="margin-left:9%;margin-right:25%;padding:25px 2%;max-width:650px;">
			<div style="background-color:#ffffff;padding:25px 25px;">
				<h3 class="heading">Get the story</h3>
				<div>
					''' + interview.description + '''<br/><br/>
					<a href="/coverage">Read our coverage</a> of this breaking story.
				</div>
				<h3>Ask questions</h3>
				Speakers can add video replies that appear in the extended interview
				<ul>''')
	for qdata in interview.questions:
		qdata = qdata.split("~|~")
		q = {"query":qdata[0],"source":qdata[1],"qid":qdata[2]}
		self.response.out.write('<li class="question">' + q["query"] + '<br/>Asked by <i>' + q["source"] + '</i></li>')
		answers = []
		for adata in interview.answers:
			adata = adata.split("~|~")
			a = {"qid":adata[0],"reply":adata[1],"source":adata[2],"video":adata[3]}
			if(a["qid"] == q["id"]):
				answers.append(a)
		for a in answers:
			self.response.out.write('<li class="response">' + a["reply"])
			if(a["video"]):
				self.response.out.write('<br/>I added a response to your question. <button class="play" onclick="gotoVid(\'' + a["video"] + '\')"><span style="font-weight:bold">&gt;</span>Watch</button>')
			self.response.out.write('<br/>Added by <i>' + a["source"] + '</i></li>')
		self.response.out.write('<hr/>')
	self.response.out.write('''				</ul>
			</div>
		</div>
		<div class="footer" style="margin-left:10%;">
			Powered by the open web technology <a href="http://popcornjs.org" target="_blank">Popcorn.js</a>
			<br/><br/>
			Developed for the Knight-Mozilla Learning Lab and TimesOpen Hack Day 2011
		</div>
	</body>
</html>''')

class Edit(webapp.RequestHandler):
  def get(self):
	interview = Interview.get_by_id(long(self.request.get('id')))
	if(interview is None):
		#self.redirect('/followfrost')
		#return
		interview = Interview()
		interview.title = "Make: Live - Maker Faire Detroit"
		interview.videos = ["youtube:z22AanAuKJQ"]
		interview.description = "Interviews with several makers and follow-ups"
		interview.tags = []
		interview.questions = []
		interview.answers = []
		interview.put()
	if(interview.description is None):
		interview.description = 'no description'
		interview.put()
	self.response.out.write('''<!DOCTYPE html>
<html>
	<head>
		<title>MoJo FollowFrost</title>
		<!-- <script type="text/javascript" src="http://mapmeld.appspot.com/popcorn.min.js"></script> -->
		<script type="text/javascript" src="http://popcornjs.org/code/dist/popcorn-complete.min.js"></script>
		<script type="text/javascript">
var myPopcorn;
function init(){
	var firstVid = "''' + interview.videos[0] + '''";
	if(firstVid.split(":")[0] == "ogg"){
		var vidEl = document.createElement('video');
		vidEl.style.width = "100%";
		vidEl.style.height = "100%";
		vidEl.src = firstVid.split(":")[1];
		vidEl.id = "popcornsite_vid";
		$("popcornsite").addChild(vidEl);
		myPopcorn = Popcorn('#popcornsite_vid');
	}
	else if(firstVid.split(":")[0] == "youtube"){
		myPopcorn = Popcorn.youtube( 'popcornsite', 'http://www.youtube.com/watch?v=' + firstVid.split(":")[1], { width: 480 } );
	}
	myPopcorn.play();
}
//dragdrop code based on http://html5demos.com/drag
function dragstart(evt,obj){
	evt.dataTransfer.effectAllowed = 'copy';
	evt.dataTransfer.setData('Text', obj.id);
}
function handleDragOver(e,obj) {
	if (e.preventDefault) e.preventDefault();
    this.className = 'over';
    e.dataTransfer.dropEffect = 'copy';
    return false;
}
function handleDragEnter(e,obj) {
  this.className = 'over';
  return false;
}
function handleDragLeave(e,obj) {
  this.className = '';
}
function handleDrop(e,obj) {
	console.log(e.dataTransfer.getData('Text'))
	if (e.stopPropagation) e.stopPropagation();
    var el = document.getElementById(e.dataTransfer.getData('Text'));
    el.parentNode.removeChild(el);
    obj.className = ''; 
    obj.appendChild(el); 
    return false;
}
function handleDragEnd(e,obj) {
   obj.removeClassName('over');
}
function jumpTo(evt){
	var time = evt.offsetX / 478 * myPopcorn.duration();
	myPopcorn.currentTime(time);
}
		</script>
		<style type="text/css">
html, body{
	font-family:tahoma;
}
div.nav{
	background-color:black;
	padding:4px;
	color:white;
	width:70%;
	margin-left:9%;
	padding-left:4%;
}
table.main{
	width:74%;
	margin-left:9%;
	margin-right:9%;
	padding-left:4%;
	padding-right:4%;
	padding-top:20px;
	padding-bottom:20px;
	background-color:#4488ff;
}
span.navitem{
	display:inline:
	margin-left:15px;
	margin-right:15px;
	padding:4px;
	background-color:black;
	color:white;
	cursor:pointer;
	text-align:center;
}
span.navitem:hover{
	color:orange;
}
span.navitem a{
	text-decoration:none;
	color:white;
}
span.navitem a:hover{
	color:orange;
}
span.selectitem{
	color:orange;
}
button{
	cursor:pointer;
}
button.watch{
	border:none;
	background-color:darkgreen;
	color:white;
}
li{
	padding:12px;
}
li.response{
	list-style-type:circle;
	margin-left:50px;
}
div.commenting{
background: #2989d8; /* Old browsers */
background: -moz-linear-gradient(top, #2989d8 0%, #2580d0 50%, #207cca 51%, #7db9e8 100%); /* FF3.6+ */
background: -webkit-gradient(linear, left top, left bottom, color-stop(0%,#2989d8), color-stop(50%,#2580d0), color-stop(51%,#207cca), color-stop(100%,#7db9e8)); /* Chrome,Safari4+ */
background: -webkit-linear-gradient(top, #2989d8 0%,#2580d0 50%,#207cca 51%,#7db9e8 100%); /* Chrome10+,Safari5.1+ */
background: -o-linear-gradient(top, #2989d8 0%,#2580d0 50%,#207cca 51%,#7db9e8 100%); /* Opera11.10+ */
background: -ms-linear-gradient(top, #2989d8 0%,#2580d0 50%,#207cca 51%,#7db9e8 100%); /* IE10+ */
filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#2989d8', endColorstr='#7db9e8',GradientType=0 ); /* IE6-9 */
background: linear-gradient(top, #2989d8 0%,#2580d0 50%,#207cca 51%,#7db9e8 100%); /* W3C */
}
img{
	max-height:220px;
	max-width:100%;
}
#tagdiv img{
	display:block;
}
.boxy{
	-moz-box-shadow: 5px 8px 15px #444444;
	-webkit-box-shadow: 5px 8px 15px #444444;
	box-shadow: 5px 8px 15px #444444;
}
.twtr-hd{
	background-color:white;
}
.twtr-doc[style]{
	width:100% !important;
}
.unhoverable:hover{
	width:0%;
}
.unhoverable:click{
	width:0%;
}
.ppllist div{
	cursor:move;
}
[draggable] {
  -moz-user-select: none;
  -khtml-user-select: none;
  -webkit-user-select: none;
  user-select: none;
}
*[draggable=true] {
  -moz-user-select:none;
  -khtml-user-drag: element;
  cursor: move;
}
*:-khtml-drag {
  background-color: rgba(238,238,238, 0.5);
}
.over {
  border: 2px dashed #000;
}
fieldset{
	background-color:#ddddff;
}
legend{
	background-color:darkblue;
	color:white;
}
		</style>
	</head>
	<body onload="init();">
		<h1 style="margin-left:14%;">FollowFrost</h1>
		<div class="nav"><nav>
			<span class="navitem selectitem">Interview</span>|
			<span class="navitem">Coverage</span>|
			<span class="navitem">
				<a href="/login">Sign In</a>
			</span>
		</nav></div>
		<table class="main">
			<tr>
				<td>
					<h3 class="heading">''' + cgi.escape(interview.title) + '''</h3>
					<div>
						<!--<div id="videooverlay" style="padding-top:15px;padding-left:35px;max-width:480px;position:absolute;background:transparent;color:#fff;">Semitransparent Text</div>-->
						<div id="popcornsite" width="480" height="360" style="padding:15px;border:3px solid black;background-color:white;margin-right:25px;margin-bottom:-60px;padding-left:25px;padding-right:25px;" src="''' + interview.videos[0] + '''">
						</div>
						<img style="display:inline;margin-left:19px;margin-top:-14px" onclick="jumpTo(event)" src="http://mapmeld.appspot.com/makerfairetrack-600.png" width="560" style="margin-top:-200px;margin-left:19px;" height="30">
					</div>
					<div style="height:140px;">
					&nbsp;
					</div>
				</td>
				<td>
					<h3 class="heading">Drag profiles in and out of video sync</h3>
					<div>
						<fieldset id="ondeckfield">
							<legend>Interview Deck</legend>
							<div id="indeck" class="pplList"  style="max-width:100%;max-height:250px;min-height:100px;min-width:50%;" ondragenter="handleDragEnter(event,this)" ondragleave="handleDragLeave(event,this)" ondragover="handleDragOver(event,this)"  ondrop="handleDrop(event,this)" ondragend="handleDragEnd(event,this)">
								<table>\n''')
	#if(interview.tags == []):
	#	interview.tags = ["mapmeld","bekathwia","MattRichardson","gonkirin","backyardbrains"]
	#	interview.put()
	divid = 0
	for ppl in interview.tags:
		divid = divid + 1
		if(divid % 2 == 1):
			self.response.out.write('									<tr><td>\n')
		else:
			self.response.out.write('									</td><td>\n')
		self.response.out.write('''<div id="tagglediv_000" class="sfy_tweet sfy_wrap" draggable="true" width="240" ondragstart="dragstart(event,this)" style="vertical-align:baseline;background-color:white;padding:3px 3px;border:1px solid #000;-moz-box-shadow:8px 8px 4px #888;-webkit-box-shadow:8px 8px 4px #888;box-shadow:8px 8px 4px #888;max-width:180px;margin:3px;">
					<div class="sfy_content" style="overflow:hidden;color:#4A4A4B;font-size:10.5pt;">
						<!--<span id="sfy_text" class="sfy_text" style="font-family:Georgia,Times New Roman,Serif;line-height:1.5;font-size:100%;color:#000;">Added to database</span>-->
						<div class="sfy_signature" style="float:right;width:250px;font-family:Arial,Helvetica;text-align:right;color:#000;"> 
							<a id="sfy_twitlink" target="_blank" style="color:#0074B7;line-height:1.3;text-align:left;" href="http://twitter.com/intent/user?screen_name=mapmeld">
								<img id="sfy_twitpic" class="sfy_thumbnail sfy_avatar" src="http://purl.org/net/spiurl/mapmeld" alt="logo" border="0" style="border: 1px solid #E9E9E9;display:inline;">
							</a>
							<div class="sfy_signature_text" style="float:right;width:auto;">
								<a id="sfy_twitlink2" href="http://twitter.com/intent/user?screen_name=mapmeld" class="twitter-anywhere-user" target="_blank" style="color:#000;text-decoration:none;">
									<span id="sfy_author" class="sfy_author" style="font-weight:bold;text-transform:none;width:auto;float:none;color:#000;font-family: Arial,Helvetica;text-decoration:none;text-align:right;">mapmeld</span>
								</a><br>
								<span class="sfy_timestamp" style="height:20px;font-size:8pt;color:#B2B4B6;">
									<img src="http://twitter.com/favicon.ico" width="16" border="0" class="sourceIcon">
									<a id="updateTime" href="2011-08-02 17:42" target="_blank" style="color:#939393;font-size:11px;">2011-08-02 17:42</a>
								</span>
							</div> 
						</div> 
					</div>
              	</div>\n'''.replace('mapmeld',ppl).replace("_000",str(divid)))
		if(divid % 2 == 0):
			self.response.out.write('</td></tr>\n')
	self.response.out.write('''								</table>
							</div>
						</fieldset>
						<fieldset id="onscreenfield">
							<legend>On Screen</legend>
							<div id="onscreen" class="pplList" style="max-width:100%;max-height:250px;min-height:100px;min-width:50%;" ondragenter="handleDragEnter(event,this)" ondragleave="handleDragLeave(event,this)" ondragover="handleDragOver(event,this)"  ondrop="handleDrop(event,this)" ondragend="handleDragEnd(event,this)">
								
							</div>
						</fieldset>
					</div>
				</td>
			</tr>
		</table>
		<div class="commenting" style="margin-left:9%;margin-right:25%;padding:25px 2%;max-width:650px;">
			<div style="background-color:#ffffff;padding:25px 25px;">
				<h3 class="heading">Get the story</h3>
				<div>
					''' + interview.description + '''<br/><br/>
					<a href="/coverage">Read our coverage</a> of this breaking story.
				</div>
				<h3>Ask questions</h3>
				Speakers can add video replies that appear in the extended interview
				<ul>''')
	for qdata in interview.questions:
		qdata = qdata.split("~|~")
		q = {"query":qdata[0],"source":qdata[1],"qid":qdata[2]}
		self.response.out.write('<li class="question">' + q["query"] + '<br/>Asked by <i>' + q["source"] + '</i></li>')
		answers = []
		for adata in interview.answers:
			adata = adata.split("~|~")
			a = {"qid":adata[0],"reply":adata[1],"source":adata[2],"video":adata[3]}
			if(a["qid"] == q["id"]):
				answers.append(a)
		for a in answers:
			self.response.out.write('<li class="response">' + a["reply"])
			if(a["video"]):
				self.response.out.write('<br/>I added a response to your question. <button class="play" onclick="gotoVid(\'' + a["video"] + '\')"><span style="font-weight:bold">&gt;</span>Watch</button>')
			self.response.out.write('<br/>Added by <i>' + a["source"] + '</i></li>')
		self.response.out.write('<hr/>')
	self.response.out.write('''				</ul>
			</div>
		</div>
		<div class="footer" style="margin-left:10%;">
			Powered by the open web technology <a href="http://popcornjs.org" target="_blank">Popcorn.js</a>
			<br/><br/>
			Developed for the Knight-Mozilla Learning Lab and TimesOpen Hack Day 2011
		</div>
	</body>
</html>''')

class Interview(db.Model):
	title = db.StringProperty(multiline=False)
	videos = db.StringListProperty()
	description = db.TextProperty()
	tags = db.StringListProperty()
	questions = db.StringListProperty()
	answers = db.StringListProperty()
	plugins = db.StringListProperty()

class Account(db.Model):
	realname = db.StringProperty(multiline=False)
	twittername = db.StringProperty(multiline=False)
	interviews = db.StringListProperty()

class VideoTag(db.Model):
	name = db.StringProperty(multiline=False)
	interviews = db.StringListProperty()

application = webapp.WSGIApplication([('/follow.*/edit', Edit),
									('/follow.*/view', View),
									('/follow.*', Home)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()