html:
	export DEBUG=False && python3 app.py &
	sleep 60
	wget -r http://127.0.0.1:8050/
	wget -r http://127.0.0.1:8050/_dash-layout
	wget -r http://127.0.0.1:8050/_dash-dependencies
	wget -r http://127.0.0.1:8050/_dash-update-component
	wget -r http://127.0.0.1:8050/_reload-hash
	sed -i 's/_dash-layout/_dash-layout.json/g' 127.0.0.1\:8050/_dash-component-suites/dash/dash-renderer/build/*.js
	sed -i 's/_dash-dependencies/_dash-dependencies.json/g' 127.0.0.1\:8050/_dash-component-suites/dash/dash-renderer/build/*.js
	sed -i 's/href="\//href="/g' 127.0.0.1\:8050/index.html
	sed -i 's/<script src="\//<script src="/g' 127.0.0.1\:8050/index.html
	sed -i 's/"requests_pathname_prefix":"\/"/"requests_pathname_prefix":"\/TWWH_db_graph"/g' 127.0.0.1\:8050/index.html

	mv 127.0.0.1:8050/_dash-layout 127.0.0.1:8050/_dash-layout.json
	mv 127.0.0.1:8050/_dash-dependencies 127.0.0.1:8050/_dash-dependencies.json

	cp assets/* 127.0.0.1:8050/assets/
	cp _static/dcc/* 127.0.0.1:8050/_dash-component-suites/dash/dcc/
	cp _static/dash_table/* 127.0.0.1:8050/_dash-component-suites/dash/dash_table/

clean:
	rm -rf 127.0.0.1:8050/

