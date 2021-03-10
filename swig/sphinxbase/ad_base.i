/* -*- c-basic-offset: 4; indent-tabs-mode: nil -*- */
/* ====================================================================
 * Copyright (c) 2013 Carnegie Mellon University.  All rights
 * reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 *
 * This work was supported in part by funding from the Defense Advanced
 * Research Projects Agency and the National Science Foundation of the
 * United States of America, and the CMU Sphinx Speech Consortium.
 *
 * THIS SOFTWARE IS PROVIDED BY CARNEGIE MELLON UNIVERSITY ``AS IS'' AND
 * ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL CARNEGIE MELLON UNIVERSITY
 * NOR ITS EMPLOYEES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * ====================================================================
 *
 */

%include pybuffer.i
%include typemaps.i

%{
#include <sphinxbase/ad.h>
typedef ad_rec_t Ad;
%}

typedef struct {} Ad;

%extend Ad {
    Ad(const char *audio_device=NULL, int sampling_rate=16000, int *errcode) {
        Ad *ad;
        if (audio_device == NULL)
            ad = ad_open_sps(sampling_rate);
        else
            ad = ad_open_dev(audio_device, sampling_rate);
        *errcode = ad ? 0 : -1;
        return ad;
    }

    ~Ad() {
        ad_close($self);
    }

    Ad *__enter__(int *errcode) {
        *errcode = ad_start_rec($self);
        return $self;
    }

    void __exit__(PyObject *exception_type, PyObject *exception_value,
                  PyObject *exception_traceback, int *errcode) {
        *errcode = ad_stop_rec($self);
    }

    int start_recording(int *errcode) {
        return *errcode = ad_start_rec($self);
    }

    int stop_recording(int *errcode) {
        return *errcode = ad_stop_rec($self);
    }

    %include <pybuffer.i>
    %pybuffer_mutable_binary(char *DATA, size_t SIZE);
    int readinto(char *DATA, size_t SIZE, int *errcode) {
        return *errcode = ad_read($self, (int16*)DATA, SIZE /= sizeof(int16));
    }
}
