$(document).ready(function() {
    $('#sidebar-menu .menu-item > span').on('click', function() {
        $(this).parent().toggleClass('open');
    });

    $('#sidebar-menu').on('click', '.submenu-item[data-type="faculty"]', function(e) {
        e.stopPropagation();
        const parent = $(this);
        const facultyId = parent.data('id');
        const departmentsList = parent.find('.nested-submenu');

        if (parent.hasClass('open')) {
            departmentsList.empty();
        } else if (departmentsList.children().length === 0) {
            $.ajax({
                url: `/api/faculties/${facultyId}/departments/`,
                type: 'GET',
                success: function(data) {
                    departmentsList.empty();
                    data.forEach(function(department) {
                        departmentsList.append(`
                            <li class="submenu-item" data-type="department" data-id="${facultyId}" data-department="${department.name}">
                                <span>${department.name}</span>
                                <ul class="nested-submenu"></ul>
                            </li>
                        `);
                    });
                },
                error: function(xhr, status, error) {
                    console.log("Error: " + error);
                    console.log("Status: " + status);
                    console.dir(xhr);
                }
            });
        }

        parent.toggleClass('open');
    });

    $('#sidebar-menu').on('click', '.submenu-item[data-type="department"]', function(e) {
        e.stopPropagation();
        const parent = $(this);
        const facultyId = parent.data('id');
        const departmentName = parent.data('department');
        const semestersList = parent.find('.nested-submenu');

        if (parent.hasClass('open')) {
            semestersList.empty();
        } else if (semestersList.children().length === 0) {
            $.ajax({
                url: `/api/faculties/${facultyId}/departments/${departmentName}/semesters/`,
                type: 'GET',
                success: function(data) {
                    semestersList.empty();
                    data.forEach(function(semester) {
                        semestersList.append(`
                            <li class="submenu-item" data-type="semester" data-id="${facultyId}" data-department="${departmentName}" data-semester="${semester.number}">
                                <span>Semestr ${semester.number}</span>
                                <ul class="nested-submenu"></ul>
                            </li>
                        `);
                    });
                },
                error: function(xhr, status, error) {
                    console.log("Error: " + error);
                    console.log("Status: " + status);
                    console.dir(xhr);
                }
            });
        }

        parent.toggleClass('open');
    });

    $('#sidebar-menu').on('click', '.submenu-item[data-type="semester"]', function(e) {
        e.stopPropagation();
        const parent = $(this);
        const facultyId = parent.data('id');
        const departmentName = parent.data('department');
        const semester = parent.data('semester');
        const groupsList = parent.find('.nested-submenu');

        if (parent.hasClass('open')) {
            groupsList.empty();
        } else if (groupsList.children().length === 0) {
            $.ajax({
                url: `/api/faculties/${facultyId}/departments/${departmentName}/semesters/${semester}/groups/`,
                type: 'GET',
                success: function(data) {
                    groupsList.empty();
                    data.forEach(function(group) {
                        groupsList.append(`<li class="submenu-item" data-type="group" data-id="${group.id}"><span>${group.name}</span></li>`);
                    });
                },
                error: function(xhr, status, error) {
                    console.log("Error: " + error);
                    console.log("Status: " + status);
                    console.dir(xhr);
                }
            });
        }

        parent.toggleClass('open');
    });

    $('#sidebar-menu').on('click', '.submenu-item[data-type="group"] > span', function(e) {
        e.stopPropagation();
        const groupId = $(this).parent().data('id');
        const groupName = $(this).text();
        $('#page-title').text(`Plan dla: ${groupName}`);
        loadSchedule(`/schedules/groups/${groupId}/schedule/`);
    });

    $('#sidebar-menu').on('click', '.submenu-item[data-type="room"] > span', function(e) {
        e.stopPropagation();
        const roomId = $(this).parent().data('id');
        const roomName = $(this).text();
        $('#page-title').text(`Plan dla: ${roomName}`);
        loadSchedule(`/schedules/rooms/${roomId}/schedule/`);
    });

    $('#sidebar-menu').on('click', '.submenu-item[data-type="teacher"] > span', function(e) {
        e.stopPropagation();
        const teacherId = $(this).parent().data('id');
        const teacherName = $(this).text();
        $('#page-title').text(`Plan dla: ${teacherName}`);
        loadSchedule(`/schedules/teachers/${teacherId}/schedule/`);
    });

    function loadSchedule(url) {
        $.ajax({
            url: url,
            type: 'GET',
            success: function(data) {
                $('.day-column').empty();
                for (let i = 8; i <= 22; i++) { // Dla każdej godziny od 8:00 do 22:00
                    const time = i < 10 ? `0${i}:00` : `${i}:00`;
                    $('.day-column').append(`<div class="hour-line" style="top: ${(i - 8) * 100}px;"></div>`);
                }
                data.forEach(function(schedule) {
                    const dayColumn = $(`#${schedule.day_of_week.toLowerCase()}`);
                    const startHour = parseInt(schedule.start_time.split(':')[0]);
                    const startMinutes = parseInt(schedule.start_time.split(':')[1]);
                    const endHour = parseInt(schedule.end_time.split(':')[0]);
                    const endMinutes = parseInt(schedule.end_time.split(':')[1]);

                    const start = startHour * 60 + startMinutes;
                    const end = endHour * 60 + endMinutes;
                    const top = (start - 480) / 60 * 100;
                    const height = (end - start) / 60 * 100;

                    dayColumn.append(`
                        <div class="schedule-item" style="top: ${top}px; height: ${height}px;">
                            <p><strong>${schedule.course_type}, ${schedule.week_type}</strong></p>
                            <p class="clickable" data-type="room" data-id="${schedule.room_id}">${schedule.room}</p>
                            <p>${schedule.course}</p>
                            <p class="clickable" data-type="teacher" data-id="${schedule.teacher_id}">${schedule.teacher}</p>
                            <p class="clickable" data-type="group" data-id="${schedule.group_id}">${schedule.group}</p>
                        </div>
                    `);
                });

                $('.clickable').on('click', function() {
                    const type = $(this).data('type');
                    const id = $(this).data('id');
                    const name = $(this).text();
                    $('#page-title').text(`Plan dla: ${name}`);
                    if (type === 'room') {
                        loadSchedule(`/schedules/rooms/${id}/schedule/`);
                    } else if (type === 'teacher') {
                        loadSchedule(`/schedules/teachers/${id}/schedule/`);
                    } else if (type === 'group') {
                        loadSchedule(`/schedules/groups/${id}/schedule/`);
                    }
                });
            },
            error: function(xhr, status, error) {
                console.log("Error: " + error);
                console.log("Status: " + status);
                console.dir(xhr);
            }
        });
    }
});
