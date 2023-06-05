-- auto-generated definition
create table music
(
    id        int auto_increment
        primary key,
    title     varchar(64)                                                                       not null,
    lyric     text                                                                              not null,
    label     enum ('happiness', 'sadness', 'neutral', 'disgust', 'fear', 'anger', 'surprised') not null,
    happiness double                                                                            not null,
    sadness   double                                                                            not null,
    neutral   double                                                                            not null,
    disgust   double                                                                            not null,
    fear      double                                                                            not null,
    anger     double                                                                            not null,
    surprised double                                                                            not null
);

create index music_label_index
    on music (label);


